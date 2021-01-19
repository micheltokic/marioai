package de.lmu.parl;

import static de.lmu.parl.proto.MarioProtos.MarioMessage;
import static de.lmu.parl.proto.MarioProtos.Init;
import static de.lmu.parl.proto.MarioProtos.Action;

import ch.idsia.benchmark.mario.environments.MarioEnvironment;
import ch.idsia.tools.MarioAIOptions;


import java.io.*;
import java.net.URISyntaxException;
import java.net.URL;

import java.util.jar.JarFile;
import java.util.Enumeration;
import java.util.jar.JarEntry;




public class Controller {

    private MarioEnvironment env = MarioEnvironment.getInstance();
    private FeatureExtractor featureExtractor = new FeatureExtractor(env);
    private MarioAIOptions options;

    private MarioMessage createStateMessage() {
        return MarioMessage.newBuilder()
                .setType(MarioMessage.Type.STATE)
                .setState(featureExtractor.getState())
                .build();
    }

    public void handleInitMessage(MarioMessage msg) {
        Init init = msg.getInit();

        // cache options
        options = buildOptions(
                init.getRFieldW(), init.getRFieldH(), init.getSeed(),
                init.getLevelLength(), init.getDifficulty(), init.getRender(), init.getFileName());

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
        env.performAction(ActionMap.actionMap.get(action));
        env.tick();

        return createStateMessage();
    }

    /*
    public void handleRenderMessage(MarioMessage msg) {
        // render() may contain a mode
        // render the environment
    }
     */

    public MarioAIOptions buildOptions(int rfw, int rfh, int randSeed, int levelLength, int difficulty, boolean render, String fileName) {
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
        //options.setArgs("-lde on -i on -ld 30 -ls 133434"); //hard level with lots of birds and enemies
        //options.setArgs("-lf on -lg on"); //easy level --> flat with no obstacles
        if(!fileName.equals("None")){

            final File jarFile = new File(getClass().getProtectionDomain().getCodeSource().getLocation().getPath());

            if(jarFile.isFile()) {  // Run with JAR file
                //URL localPackage = this.getClass().getResource("");
                //System.out.println(localPackage.getPath());
                //String[] pathArray = localPackage.getPath().split("de/");
                //String[] pathArray2 = pathArray[0].split("e:/");
                //System.out.println(pathArray2[0]+"\r\n" + pathArray2[1]); // + "\r\n" + pathArray[2]);
                //System.out.println(" -ls "+pathArray2[1]+"Levels/"+fileName);
                //options.setArgs(" -ls "+pathArray2[1]+"Levels/"+fileName);
                //try{
                //    File file = new File(getClass().getResource("/Levels/"+fileName).toURI());
                //    options.setArgs(" -ls "+file.getPath());
                //}catch(java.net.URISyntaxException e){
                //    System.out.println("Exeption: "+e);
                //}
                System.out.println("Stable level selection is currently not possible");
                if (fileName.equals("easyLevel.lvl")){
                    options.setArgs("-lf on -lg on");
                }else if (fileName.equals("flatLevel.lvl")){
                    options.setFlatLevel(true);
                }else if (fileName.equals("hardLevel.lvl")){
                    options.setArgs("-lde on -i on -ld 30 -ls 133434");
                }

            } else { // Run with IDE
                options.setArgs(" -ls target/classes/Levels/"+fileName);
            }
            // File file = new File(getClass().getResource("/Levels/"+fileName).getPath());
            //System.out.println("Test100: "+file);

        };

        return options;
    }
}
