package de.lmu.parl;

import ch.idsia.benchmark.mario.engine.sprites.Mario;
import ch.idsia.benchmark.mario.environments.MarioEnvironment;
import ch.idsia.tools.MarioAIOptions;
import de.lmu.parl.proto.MarioProtos;
import de.lmu.parl.proto.MarioProtos.State;
import de.lmu.parl.proto.MarioProtos.ReceptiveFieldCell;

public class FeatureExtraction {

    public static final int cellSize = 16;
    public static final int corners = 4;

    public static final int greyStone = 9;
    public static final int destructibleRock = 16;
    public static final int indestructibleRock = 17;
    public static final int questionMark = 21;
    public static final int greenPipe = 53;

    public static final int coin = 34;

    public static State getState (MarioEnvironment env) {
        Mario mario = env.getMario();
        byte[][] level = env.getLevel().map;
        int rfw = env.getReceptiveFieldWidth();
        int rfh = env.getReceptiveFieldHeight();
        float[] enemies = env.getEnemiesFloatPos();

        byte[][][] levelScene = rfLevelScene(mario, level, rfw, rfh);
        boolean[][] rfObstacle = rfObstacle(levelScene);
        boolean[][] rfCoins = rfCoins(levelScene);
        boolean[][] rfQms = rfQuestionMarks(levelScene);
        boolean[][] rfEnemies = rfEnemies(enemies, rfw, rfh);

        State.Builder stateBuilder = State.newBuilder();
        stateBuilder.setGameStatusValue(mario.getStatus());
        for (int y = 0; y < rfh; y++){
            for (int x = 0; x < rfw; x++) {
                ReceptiveFieldCell.Builder rFBuilder = ReceptiveFieldCell.newBuilder();
                rFBuilder.setCoin(rfCoins[y][x]);
                rFBuilder.setEnemy(rfEnemies[y][x]);
                rFBuilder.setObstacle(rfObstacle[y][x]);
                rFBuilder.setItembox(rfQms[y][x]);
                stateBuilder.addReceptiveFields(rFBuilder);
            }
        }

        return stateBuilder.build();
    }

    public static byte[][][] rfLevelScene(Mario mario, byte[][] level, int rfw, int rfh) {

        byte[][][] receptiveField = new byte[rfh][rfw][4]; // check all 4 corners of receptive field for level indices

        int cellsLeft = rfw / 2;
        int cellsAbove = (rfh / 2) + 1;

        for(int x = 0; x < rfw; x++) {
            for(int y = 0; y < rfh; y++) {
                int leftX = floatToIndex(mario.x -cellsLeft*cellSize + x*cellSize);
                int rightX = leftX + 1;
                int topY = floatToIndex(mario.y -cellsAbove*cellSize + y*cellSize);
                int botY = topY + 1;

                if(!(leftX < 0 || topY < 0 || leftX >= level.length || topY >= level[0].length)){
                    receptiveField[y][x][0] = level[leftX][topY];
                }
                if(!(leftX < 0 || botY < 0 || leftX >= level.length || botY >= level[0].length)){
                    receptiveField[y][x][1] = level[leftX][botY];
                }
                if(!(rightX < 0 || topY < 0 || rightX >= level.length || topY >= level[0].length)){
                    receptiveField[y][x][2] = level[rightX][topY];
                }
                if(!(rightX < 0 || botY < 0 || rightX >= level.length || botY >= level[0].length)){
                    receptiveField[y][x][3] = level[rightX][botY];
                }
            }
        }

        return receptiveField;
    }

    public static boolean[][] rfObstacle(byte[][][] levelScene) {
        int rfh = levelScene.length;
        int rfw = levelScene[0].length;
        boolean[][] rfObstacle = new boolean[rfh][rfw];
        for(int x = 0; x < rfw; x++){
            for(int y = 0; y < rfh; y++) {
                for(int corner=0; corner<corners; corner++){
                    byte tile = levelScene[y][x][corner];
                    if(tile == greyStone ||
                            tile == greenPipe ||
                            tile == questionMark ||
                            tile == destructibleRock ||
                            tile == indestructibleRock)
                    {
                        rfObstacle[y][x] = true;
                        break;
                    }
                }
            }
        }
        return rfObstacle;
    }

    public static boolean[][] rfCoins(byte[][][] levelScene){
        int rfh = levelScene.length;
        int rfw = levelScene[0].length;
        boolean[][] rfCoins = new boolean[rfh][rfw];
        for(int x = 0; x < rfw; x++){
            for(int y = 0; y < rfh; y++) {
                for(int corner=0; corner<corners; corner++){
                    byte tile = levelScene[y][x][corner];
                    if(tile == coin) {
                        rfCoins[y][x] = true;
                        break;
                    }
                }
            }
        }
        return rfCoins;
    }

    public static boolean[][] rfQuestionMarks(byte[][][] levelScene){
        int rfh = levelScene.length;
        int rfw = levelScene[0].length;
        boolean[][] rfQms = new boolean[rfh][rfw];
        for(int x = 0; x < rfw; x++){
            for(int y = 0; y < rfh; y++) {
                for(int corner=0; corner<4; corner++){
                    byte tile = levelScene[y][x][corner];
                    if(tile == questionMark) {
                        rfQms[y][x] = true;
                        break;
                    }
                }
            }
        }
        return rfQms;
    }

    public static boolean[][] rfEnemies(float[] enemies, int rfw, int rfh) {
        boolean[][] rfEnemies = new boolean[rfh][rfw];

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

        return rfEnemies;
    }

    public static int floatToIndex(float pos) {
        return (int) (pos / cellSize);
    }



    public static void main(String[] args) {
        MarioEnvironment env = MarioEnvironment.getInstance();
        int rfw = 11;
        int rfh = 5;
        MarioAIOptions options = new Controller().buildOptions(
                rfw, rfh, 1000, 80, 0, true
        );

        env.reset(options);
        for (int i = 0; i < 100; i++) {
            float[] marioFloatPos = env.getMarioFloatPos();
            float[] enemiesFloat = env.getEnemiesFloatPos();

            env.performAction(new boolean[]{false, true, false, i%2==0, false, false});
            env.tick();

            Mario mario = env.getMario();
            byte[][] level = env.getLevel().map;

            byte[][][] rfLevelScene = rfLevelScene(mario, level, rfw, rfh);
            boolean[][] rfObstacle = rfObstacle(rfLevelScene);
            boolean[][] rfCoins = rfCoins(rfLevelScene);
            boolean[][] rfQms = rfQuestionMarks(rfLevelScene);
            boolean[][] rfEnemies = rfEnemies(enemiesFloat, rfw, rfh);

            MarioProtos.State state = getState(env);
            System.out.println("");

        }
        System.out.println("debug");
    }
}
