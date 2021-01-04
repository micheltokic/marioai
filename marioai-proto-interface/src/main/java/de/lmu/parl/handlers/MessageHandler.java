package de.lmu.parl.handlers;

import static de.lmu.parl.proto.MarioProtos.MarioMessage;
import static de.lmu.parl.proto.MarioProtos.Init;
import static de.lmu.parl.proto.MarioProtos.Action;
import static de.lmu.parl.proto.MarioProtos.State;

import ch.idsia.benchmark.mario.engine.sprites.Mario;
import ch.idsia.benchmark.mario.environments.MarioEnvironment;
import ch.idsia.tools.MarioAIOptions;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;

public class MessageHandler extends SimpleChannelInboundHandler<MarioMessage> {

    private MarioEnvironment marioEnvironment = MarioEnvironment.getInstance();
    private MarioAIOptions marioAIOptions;
    private State state;

    public MarioMessage handleInitMessage(MarioMessage msg) {
        Init init = msg.getInit();
        marioAIOptions = buildOptions(
                init.getRFieldW(), init.getRFieldH(), init.getSeed(),
                init.getLevelLength(), init.getDifficulty());

        marioEnvironment.reset(this.marioAIOptions);
        marioEnvironment.tick();

        // Random answer, work in progress
        state = State.newBuilder().setState(42).build();
        return MarioMessage.newBuilder()
                .setType(MarioMessage.Type.STATE)
                .setState(state).build();
    }

    public MarioMessage handleActionMessage(MarioMessage msg) {
        Action action = msg.getAction();
        boolean[] actionArray = new boolean[]{
                action.getUp(), action.getRight(), action.getDown(),
                action.getLeft(), action.getSpeed(), action.getJump()};
        marioEnvironment.performAction(actionArray);
        marioEnvironment.tick();

        // Random answer, work in progress
        state = State.newBuilder().setState(42).build();
        return MarioMessage.newBuilder()
                .setType(MarioMessage.Type.STATE)
                .setState(state).build();
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) { // (2)
        try {
            MarioMessage marioMessage = (MarioMessage) msg;
            switch (marioMessage.getType()) {
                case INIT:
                    MarioMessage response = handleInitMessage(marioMessage);
                    ctx.writeAndFlush(response);
                    break;
                case ACTION:
                    MarioMessage state = handleActionMessage(marioMessage);
                    ctx.writeAndFlush(state);
            }
        } catch (ClassCastException e) {
            e.printStackTrace();
            ctx.close();
        }
    }

    protected void channelRead0(ChannelHandlerContext channelHandlerContext, MarioMessage msg) throws Exception {
        System.out.println(msg);
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) { // (4)
        // Close the connection when an exception is raised.
        cause.printStackTrace();
        ctx.close();
    }

    public MarioAIOptions buildOptions(int rfw, int rfh, int randSeed, int levelLength, int difficulty) {
        int viewHeight=320; // pixels
        int viewWidth=1600; // pixels
        MarioAIOptions options = new MarioAIOptions(
                " -vh " + viewHeight +
                        " -vw " + viewWidth +
                        " -srf on " +
                        " -rfw " + rfw +
                        " -rfh " + rfh);
        options.setFlatLevel(false);
        options.setBlocksCount(true);
        options.setCoinsCount(true);
        options.setLevelRandSeed(randSeed); // comment out for random levels
        options.setVisualization(true); // false: no visualization => faster learning
        options.setGapsCount(true);
        options.setMarioMode(2);
        options.setLevelLength(levelLength);
        options.setCannonsCount(true);
        options.setTimeLimit(100);
        options.setDeadEndsCount(false);
        options.setTubesCount(false);
        options.setLevelDifficulty(difficulty);
        return options;
    }
}
