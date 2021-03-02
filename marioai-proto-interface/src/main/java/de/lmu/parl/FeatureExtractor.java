package de.lmu.parl;

import ch.idsia.benchmark.mario.engine.GeneralizerLevelScene;
import ch.idsia.benchmark.mario.engine.sprites.Mario;
import ch.idsia.benchmark.mario.environments.MarioEnvironment;
import ch.idsia.tools.MarioAIOptions;
import com.google.protobuf.ByteString;
import de.lmu.parl.proto.MarioProtos;
import de.lmu.parl.proto.MarioProtos.State;
import de.lmu.parl.proto.MarioProtos.ReceptiveFieldCell;

import java.util.Arrays;
import java.util.HashMap;


public class FeatureExtractor {

    private HashMap<Integer, Boolean> sentStates = new HashMap<>();

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

    public void reset() {
        sentStates = new HashMap<>();
    }

    public State getState (boolean compact) {
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

        // receptive field cells
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

        State.MarioPosition position;
        if (mario.isOnGround()) {
            position = State.MarioPosition.FLOOR;
        } else {
            position = isOverCliff(mario, level) ? State.MarioPosition.CLIFF : State.MarioPosition.AIR;
        }
        stateBuilder.setPosition(position);

        //int hashCode = stateBuilder.build().hashCode();
        //int hashCode = new StateHash(rfObstacles, rfEnemies, rfCoins, rfQms).hashCode();
        int hashCode = 17;
        hashCode = 31 * hashCode + Arrays.deepHashCode(rfObstacles);
        hashCode = 31 * hashCode + Arrays.deepHashCode(rfEnemies);
        hashCode = 31 * hashCode + Arrays.deepHashCode(rfCoins);
        hashCode = 31 * hashCode + Arrays.deepHashCode(rfQms);
        System.out.println(hashCode);

        ////////////////////////////////////////////////////////
        // general additional information, not included in the receptive field
        ///////////////////////////////////////////////////////
        stateBuilder.setKillsByFire(env.getKillsByFire())
                .setKillsByStomp(env.getKillsByStomp())
                .setKillsByShell(env.getKillsByShell())
                .setMarioX(mario.mapX)
                .setMarioY(mario.mapY)
                .setGameStatusValue(mario.getStatus())
                .setModeValue(mario.getMode());

        if(compact) {
            if(sentStates.containsKey(hashCode)) {
                State.Builder returnStateBuilder = State.newBuilder();
                returnStateBuilder.setPosition(position);
                returnStateBuilder.setKillsByFire(env.getKillsByFire())
                        .setKillsByStomp(env.getKillsByStomp())
                        .setKillsByShell(env.getKillsByShell())
                        .setMarioX(mario.mapX)
                        .setMarioY(mario.mapY)
                        .setGameStatusValue(mario.getStatus())
                        .setModeValue(mario.getMode())
                        .setHashCode(hashCode);
                return returnStateBuilder.build();
            } else {
                // Use the same builder that was used for hash generation
                // if state was sent for the first time
                stateBuilder.setHashCode(hashCode);
                sentStates.put(hashCode, true);
            }
        }

        return stateBuilder.build();
    }

    public ByteString getRfCompact(boolean[][] rfObstacles, boolean[][] rfEnemies, boolean[][] rfCoins, boolean[][] rfQms,
                              int rfw, int rfh) {

        int numBytes = (int) Math.ceil(((double) rfw * rfh * 4) / 8.0);

        byte[] bytes = new byte[numBytes];

        byte b1 = 1;
        byte b2 = 2;
        byte b3 = 4;
        byte b4 = 8;
        byte b5 = 16;
        byte b6 = 32;
        byte b7 = 64;
        byte b8 = (byte) 128;

        for (int y = 0; y < rfh; y++) {
            for (int x = 0; x < rfw; x++) {
                int cellIndex = y * rfw + x;
                int i = cellIndex / 2;

                if (cellIndex % 2 == 0) {
                    // set the first 4 bits
                    if (rfObstacles[y][x]) bytes[i] |= b1;
                    if (rfEnemies[y][x]) bytes[i] |= b2;
                    if (rfCoins[y][x]) bytes[i] |= b3;
                    if (rfQms[y][x]) bytes[i] |= b4;

                } else {
                    // set the second 4 bits
                    if (rfObstacles[y][x]) bytes[i] |= b5;
                    if (rfEnemies[y][x])   bytes[i] |= b6;
                    if (rfCoins[y][x])     bytes[i] |= b7;
                    if (rfQms[y][x])       bytes[i] |= b8;
                }
            }
        }

        return ByteString.copyFrom(bytes);
    }

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

    private static boolean isQuestionMark(byte tile) {
        switch (tile) {
            case 21:
            case 22:
            case 23:
                return true;
        }
        return false;
    }

    private static boolean isGround(byte tile) {
        return isObstacle(tile) || tile == GeneralizerLevelScene.BORDER_HILL;
    }

    private static boolean isOverCliff (Mario mario, byte[][] level) {
        int marioX = floatToIndex(mario.x);
        if(marioX >= level.length) return false;

        int marioY = floatToIndex(mario.y);
        for(int i=marioY; i<level[marioX].length; i++) {
            byte tile = GeneralizerLevelScene.ZLevelGeneralization(level[marioX][i], 1);
            if(isGround(tile)) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        MarioEnvironment env = MarioEnvironment.getInstance();
        int rfw = 11;
        int rfh = 5;
        MarioAIOptions options = new Controller().buildOptions(
                rfw, rfh, 1000, 80, 0, true, "none"
        );

        env.reset(options);
        for (int i = 0; i < 100; i++) {
            FeatureExtractor extractor = new FeatureExtractor(env);

            float[] marioFloatPos = env.getMarioFloatPos();
            float[] enemiesFloat = env.getEnemiesFloatPos();

            env.performAction(new boolean[]{false, true, false, i%2==0, false, false});
            env.tick();

            MarioProtos.State state = extractor.getState(false);
            int x = 0;
        }
        System.out.println("debug");
    }
}
