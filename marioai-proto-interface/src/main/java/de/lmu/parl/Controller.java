package de.lmu.parl;

import static de.lmu.parl.proto.MarioProtos.MarioMessage;
import static de.lmu.parl.proto.MarioProtos.Init;
import static de.lmu.parl.proto.MarioProtos.Action;

import ch.idsia.benchmark.mario.environments.MarioEnvironment;
import ch.idsia.tools.MarioAIOptions;


public class Controller {

    private MarioEnvironment env = MarioEnvironment.getInstance();
    private MarioAIOptions options;

    private MarioMessage createStateMessage() {
        return MarioMessage.newBuilder()
                .setType(MarioMessage.Type.STATE)
                .setState(FeatureExtraction.getState(env))
                .build();
    }

    public void handleInitMessage(MarioMessage msg) {
        Init init = msg.getInit();

        // cache options
        options = buildOptions(
                init.getRFieldW(), init.getRFieldH(), init.getSeed(),
                init.getLevelLength(), init.getDifficulty(), init.getRender());

        env.reset(options);
        env.tick();
    }

    public MarioMessage handleResetMessage() {
        env.reset(options);
        env.tick();

        return createStateMessage();
    }

    public MarioMessage handleActionMessage(MarioMessage msg) {
        Action action = msg.getAction();
        boolean[] actionArray = new boolean[]{
                action.getUp(), action.getRight(), action.getDown(),
                action.getLeft(), action.getSpeed(), action.getJump()};

        env.performAction(actionArray);
        env.tick();

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
