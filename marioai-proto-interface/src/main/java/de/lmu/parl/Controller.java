package de.lmu.parl;

import static de.lmu.parl.proto.MarioProtos.MarioMessage;
import static de.lmu.parl.proto.MarioProtos.Init;
import static de.lmu.parl.proto.MarioProtos.Action;
import static de.lmu.parl.proto.MarioProtos.State;
import static de.lmu.parl.proto.MarioProtos.ReceptiveFieldCell;

import ch.idsia.benchmark.mario.engine.sprites.Mario;
import ch.idsia.benchmark.mario.environments.MarioEnvironment;
import ch.idsia.tools.MarioAIOptions;

public class Controller {

    private MarioEnvironment marioEnvironment = MarioEnvironment.getInstance();
    private MarioAIOptions marioAIOptions;

    private MarioMessage createStateMessage() {

        // TODO extract and send all state information
        // example of how to build a ReceptiveFieldCell instance
        ReceptiveFieldCell cell0 = ReceptiveFieldCell.newBuilder()
                .setObstacle(true).build();

        State.Builder stateBuilder = State.newBuilder();
        stateBuilder.addReceptiveFields(cell0);

        // is mario dead or alive?
        switch (marioEnvironment.getMarioStatus()) {
            case Mario.STATUS_RUNNING:
                stateBuilder.setGameStatus(State.GameStatus.RUNNING);
                break;
            case Mario.STATUS_WIN:
                stateBuilder.setGameStatus(State.GameStatus.WON);
                break;
            case Mario.STATUS_DEAD:
                stateBuilder.setGameStatus(State.GameStatus.LOST);
                break;
        }

        return MarioMessage.newBuilder()
                .setType(MarioMessage.Type.STATE)
                .setState(stateBuilder.build())
                .build();
    }

    public void handleInitMessage(MarioMessage msg) {
        Init init = msg.getInit();

        // cache options
        marioAIOptions = buildOptions(
                init.getRFieldW(), init.getRFieldH(), init.getSeed(),
                init.getLevelLength(), init.getDifficulty(), init.getRender());

        marioEnvironment.reset(marioAIOptions);
        marioEnvironment.tick();
        // no reply required
    }

    public MarioMessage handleResetMessage() {
        marioEnvironment.reset(this.marioAIOptions);
        marioEnvironment.tick();

        return createStateMessage();
    }

    public MarioMessage handleActionMessage(MarioMessage msg) {
        Action action = msg.getAction();
        boolean[] actionArray = new boolean[]{
                action.getUp(), action.getRight(), action.getDown(),
                action.getLeft(), action.getSpeed(), action.getJump()};

        marioEnvironment.performAction(actionArray);
        marioEnvironment.tick();

        return createStateMessage();
    }

    /*
    public void handleRenderMessage(MarioMessage msg) {
        // render() may contain a mode
        // render the environment
    }
     */

    public MarioAIOptions buildOptions(int rfw, int rfh, int randSeed, int levelLength, int difficulty, boolean render) {
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
        options.setVisualization(render); // false: no visualization => faster learning
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
