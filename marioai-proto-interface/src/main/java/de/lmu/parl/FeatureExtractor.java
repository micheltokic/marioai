package de.lmu.parl;

import ch.idsia.benchmark.mario.engine.GeneralizerLevelScene;
import ch.idsia.benchmark.mario.engine.sprites.Mario;
import ch.idsia.benchmark.mario.environments.MarioEnvironment;
import ch.idsia.tools.MarioAIOptions;
import de.lmu.parl.proto.MarioProtos;
import de.lmu.parl.proto.MarioProtos.State;
import de.lmu.parl.proto.MarioProtos.ReceptiveFieldCell;
import org.junit.Test;

public class FeatureExtractor {

    public static final int cellSize = 16;

    public static final int questionMark = 21;
    public static final int coin = 34;

    public boolean [][] rfObstacles;
    public boolean [][] rfEnemies;
    public boolean [][] rfCoins;
    public boolean [][] rfQms;

    private MarioEnvironment env;

    public FeatureExtractor(MarioEnvironment env) {
        this.env = env;
    }

    public State getState () {
        Mario mario = env.getMario();
        byte[][] level = env.getLevel().map;
        int rfw = env.getReceptiveFieldWidth();
        int rfh = env.getReceptiveFieldHeight();
        float[] enemies = env.getEnemiesFloatPos();

        rfObstacles = new boolean[rfh][rfw];
        rfEnemies = new boolean[rfh][rfw];
        rfCoins = new boolean[rfh][rfw];
        rfQms = new boolean[rfh][rfw];

        byte[][] levelScene = extractLevelScene(mario, level, rfw, rfh);
        extractMapTiles(levelScene);
        extractEnemies(enemies, rfw, rfh);

        State.Builder stateBuilder = State.newBuilder();
        stateBuilder.setGameStatusValue(mario.getStatus());
        for (int y = 0; y < rfh; y++){
            for (int x = 0; x < rfw; x++) {
                ReceptiveFieldCell.Builder rFBuilder = ReceptiveFieldCell.newBuilder();
                rFBuilder.setCoin(rfCoins[y][x]);
                rFBuilder.setEnemy(rfEnemies[y][x]);
                rFBuilder.setObstacle(rfObstacles[y][x]);
                rFBuilder.setItembox(rfQms[y][x]);
                stateBuilder.addReceptiveFields(rFBuilder);
            }
        }

        ////////////////////////////////////////////////////////
        // general additional information, not included in the receptive field
        ///////////////////////////////////////////////////////
        stateBuilder.setKillsByFire(env.getKillsByFire())
                    .setKillsByStomp(env.getKillsByStomp())
                    .setKillsByShell(env.getKillsByShell())

                    .setMarioX(mario.mapX)
                    .setMarioY(mario.mapY)
                    .setModeValue(mario.getMode());


        return stateBuilder.build();
    }

//    public static byte[][][] rfLevelScene(Mario mario, byte[][] level, int rfw, int rfh) {
//
//        byte[][][] receptiveField = new byte[rfh][rfw][4]; // check all 4 corners of receptive field for level indices
//
//        int cellsLeft = rfw / 2;
//        int cellsAbove = (rfh / 2) + 1;
//
//        for(int x = 0; x < rfw; x++) {
//            for(int y = 0; y < rfh; y++) {
//                int leftX = floatToIndex(mario.x -cellsLeft*cellSize + x*cellSize);
//                int rightX = leftX + 1;
//                int topY = floatToIndex(mario.y -cellsAbove*cellSize + y*cellSize);
//                int botY = topY + 1;
//
//                if(!(leftX < 0 || topY < 0 || leftX >= level.length || topY >= level[0].length)){
//                    receptiveField[y][x][0] = level[leftX][topY];
//                }
//                if(!(leftX < 0 || botY < 0 || leftX >= level.length || botY >= level[0].length)){
//                    receptiveField[y][x][1] = level[leftX][botY];
//                }
//                if(!(rightX < 0 || topY < 0 || rightX >= level.length || topY >= level[0].length)){
//                    receptiveField[y][x][2] = level[rightX][topY];
//                }
//                if(!(rightX < 0 || botY < 0 || rightX >= level.length || botY >= level[0].length)){
//                    receptiveField[y][x][3] = level[rightX][botY];
//                }
//            }
//        }
//
//        return receptiveField;
//    }

    public byte[][] extractLevelScene(Mario mario, byte[][] level, int rfw, int rfh) {

        byte[][] receptiveField = new byte[rfh][rfw]; // check all 4 corners of receptive field for level indices

        int cellsLeft = rfw / 2;
        int cellsAbove = (rfh / 2) + 1;

        for(int x = 0; x < rfw; x++) {
            for(int y = 0; y < rfh; y++) {
                int centerX = floatToIndex(mario.x -cellsLeft*cellSize + x*cellSize + 0.5f*cellSize);
                int centerY = floatToIndex(mario.y -cellsAbove*cellSize + y*cellSize + 0.5f*cellSize);

                if(!(centerX < 0 || centerY < 0 || centerX >= level.length || centerY >= level[0].length)){
                    receptiveField[y][x] = level[centerX][centerY];
                }
            }
        }

        return receptiveField;
    }

    public void extractMapTiles(byte[][] levelScene) {
        int rfh = levelScene.length;
        int rfw = levelScene[0].length;
        for(int x = 0; x < rfw; x++){
            for(int y = 0; y < rfh; y++) {
                byte tile = levelScene[y][x];
                if(isObstacle(GeneralizerLevelScene.ZLevelGeneralization(tile, 1))) {
                    rfObstacles[y][x] = true;
                }
                if(isQuestionMark(tile)) {
                    rfQms[y][x] = true;
                } else if(tile == coin) {
                    rfCoins[y][x] = true;
                }

            }
        }
    }

    public void extractEnemies(float[] enemies, int rfw, int rfh) {
        float[][] enemiesSplit = new float[enemies.length / 3][2];
        for(int i=0; i<enemies.length; i++){
            if(i%3==0){
                continue;
            } else if (i%3==1){
                enemiesSplit[i/3][0] = enemies[i];
            } else {
                enemiesSplit[i/3][1] = enemies[i] - (float)(cellSize / 2); // move up by half a cell to "center" the enemy
            }
        }

        int cellsLeft = rfw / 2;
        int cellsAbove = (rfh / 2) + 1;

        for(int x = 0; x < rfw; x++) {
            for(int y = 0; y < rfh; y++) {
                float leftX = -cellsLeft*cellSize + x*cellSize;
                float rightX = leftX + cellSize;
                float topY = -cellsAbove*cellSize + y*cellSize;
                float botY = topY + cellSize;

                for(float[] enemy: enemiesSplit){
                    if (enemy[0] > leftX && enemy[0] <= rightX &&
                            enemy[1] > topY && enemy[1] <= botY) {
                        rfEnemies[y][x] = true;
                        break;
                    }
                }
            }
        }
    }

    public static int floatToIndex(float pos) {
        return (int) (pos / cellSize);
    }

    private static boolean isObstacle(byte tile) {
        switch(tile) {
            case GeneralizerLevelScene.BRICK:
            case GeneralizerLevelScene.BORDER_CANNOT_PASS_THROUGH:
            case GeneralizerLevelScene.FLOWER_POT_OR_CANNON:
            case GeneralizerLevelScene.LADDER:
                return true;
        }
        return false;
    }

    private static boolean isGround(byte tile) {
        return isObstacle(tile) || tile == GeneralizerLevelScene.BORDER_HILL;
    }

    private static boolean isQuestionMark(byte tile) {
        switch (tile) {
            case 21:
            case 22:
            case 23:
                return true;
        }
        return false;
    }



    public static void main(String[] args) {
        MarioEnvironment env = MarioEnvironment.getInstance();
        int rfw = 11;
        int rfh = 5;
        MarioAIOptions options = new Controller().buildOptions(
                rfw, rfh, 1000, 80, 0, true, "flatLevel.lvl"
        );

        env.reset(options);
        for (int i = 0; i < 100; i++) {
            FeatureExtractor extractor = new FeatureExtractor(env);

            float[] marioFloatPos = env.getMarioFloatPos();
            float[] enemiesFloat = env.getEnemiesFloatPos();

            env.performAction(new boolean[]{false, true, false, i%2==0, false, false});
            env.tick();

            MarioProtos.State state = extractor.getState();
            int x = 0;
        }
        System.out.println("debug");
    }
}
