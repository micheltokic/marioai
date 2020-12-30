package apidemo;


import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.LinkedHashMap;
import java.util.Map.Entry;
import java.util.Random;

import org.hswgt.teachingbox.core.rl.datastructures.ActionSet;
import org.hswgt.teachingbox.core.rl.env.Action;

import ch.idsia.benchmark.mario.engine.GeneralizerLevelScene;
import ch.idsia.benchmark.mario.engine.GlobalOptions;
import ch.idsia.benchmark.mario.engine.sprites.Mario;
import ch.idsia.benchmark.mario.engine.sprites.Sprite;
import ch.idsia.benchmark.mario.environments.MarioEnvironment;
import ch.idsia.tools.MarioAIOptions;

public class ApiDemo {
	
	// Actions
	public static final ActionSet ACTION_SET = new ActionSet();	
	protected static LinkedHashMap <Action, String> ACTIONS = new LinkedHashMap<Action, String>();
	protected static LinkedHashMap <String, Action> ACTION_MAP = new LinkedHashMap<String,Action>();
	static {
		//ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_LEFT)}), "LEFT");
		//ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_RIGHT)}), "RIGHT");
		//ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_UP)}), "UP");
		ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_DOWN)}), "DOWN");
		ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_JUMP)}), "JUMP");
		//ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_SPEED)}), "SPEED");
		
		ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_SPEED | 1<< Mario.KEY_JUMP)}), "SPEED_JUMP");
		ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_SPEED | 1<< Mario.KEY_RIGHT)}), "SPEED_RIGHT");
		ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_SPEED | 1<< Mario.KEY_LEFT)}), "SPEED_LEFT");
		
		ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_JUMP | 1<< Mario.KEY_RIGHT)}), "JUMP_RIGHT");
		ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_JUMP | 1<< Mario.KEY_LEFT)}), "JUMP_LEFT");
		
		ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_JUMP | 1<< Mario.KEY_SPEED | 1<< Mario.KEY_RIGHT)}), "JUMP_SPEED_RIGHT");
		ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_JUMP | 1<< Mario.KEY_SPEED | 1<< Mario.KEY_LEFT)}), "JUMP_SPEED_LEFT");
		
        for (Entry <Action, String> e : ACTIONS.entrySet()) {
			ACTION_SET.add(e.getKey());
			ACTION_MAP.put(e.getValue(), e.getKey());
        }
	}
	
	private static MarioEnvironment environment = MarioEnvironment.getInstance();
	
	private static int levelRandSeed = 1000;
	private static Random randGen = new Random();
	
	public static void main(String[] args) {
		
		// setup level options
		//MarioAIOptions marioAIOptions = new MarioAIOptions("-vh 240 -vw 320 -srf on -rfw 5 -rfh 5");
		int receptiveFieldHeight = 5;  // rows
		int receptiveFieldWidth = 11;  // columns
		int viewHeight=320; // pixels
		int viewWidth=1600; // pixels
		MarioAIOptions marioAIOptions = new MarioAIOptions(
					" -vh " + viewHeight + 
					" -vw " + viewWidth + 
					" -srf on " + 
					" -rfw " + receptiveFieldWidth + 
					" -rfh " + receptiveFieldHeight);
		
		marioAIOptions.setFlatLevel(false);
		marioAIOptions.setBlocksCount(true);
		marioAIOptions.setCoinsCount(true);
		marioAIOptions.setLevelRandSeed(levelRandSeed); // comment out for random levels
		marioAIOptions.setVisualization(true); // false: no visualization => faster learning
		marioAIOptions.setGapsCount(true);
		marioAIOptions.setMarioMode(2);
		marioAIOptions.setLevelLength(80);
		marioAIOptions.setCannonsCount(true);
		marioAIOptions.setTimeLimit(100);
		marioAIOptions.setDeadEndsCount(false);
		marioAIOptions.setTubesCount(false);
		marioAIOptions.setLevelDifficulty(2);
		//marioAIOptions.setScale2X(true); // does only work for 240x320

		
		System.out.println("Options: " + marioAIOptions.asString());
	    marioAIOptions.printOptions(true);

		// setup engine 
		ApiAgent agent = new ApiAgent();
		marioAIOptions.setAgent(agent); 

		System.out.println("CMD Options: " + marioAIOptions.toString());
		
		// reset agent
	    environment.reset(marioAIOptions); 
	    
	    boolean[] marioAiAction = new boolean[ch.idsia.benchmark.mario.environments.Environment.numberOfKeys];
	    double totalReward = -1;
	    
	    // do some actions
		for (int step=0; step<1000; step++) {
			
			// chose random action
			String actionName = (String)ACTION_MAP.keySet().toArray()[randGen.nextInt(ACTION_MAP.keySet().size())];
			System.out.println ("Performing action (no. " + step + "): " + actionName);
			Action a = ACTION_MAP.get(actionName);
			for (int i=0; i<ch.idsia.benchmark.mario.environments.Environment.numberOfKeys; i++) {
				marioAiAction[i] = ((int)a.get(0) & (1<<i)) > 0 ? true : false;
			}
			agent.setAction(marioAiAction);
			
			// perform action
			environment.performAction(agent.getAction());
			//marioAIOptions.setReceptiveFieldVisualized(true);
			
			// update environment
	    	environment.tick();
	        agent.integrateObservation(environment);	
	        
	        // 1) reward
	        double rewardDiff = environment.getIntermediateReward() - totalReward;
	        totalReward = environment.getIntermediateReward();
	        System.out.println("  -> Reward: " + rewardDiff + " - totalReward=" + totalReward);
	        // other stuff: 
	        // environment.getKilledCreaturesByFireBall();
	        // environemtn.getKilled .... 
	        
	        // 2) position
	        float[] pos = environment.getMarioFloatPos();
	        float marioX = pos[0];
	        float marioY = pos[1];
	        System.out.println("  -> MarioPos: x=" + marioX + ", y=" + marioY);
	        
	        // 3) investigate scene for enemies/obstacles ...
	        byte[][] scene = environment.getMergedObservationZZ(1, 1);
	        // isObstacle(scene, x, y)
	        // isGround (scene, x, y)
	        //if (scene[y][x] == Sprite.KIND_GOOMBA ||
			//	scene[y][x] == Sprite.KIND_SPIKY /* .... */) {
	        
	        // 4) is mario able to jump?	   
	        boolean canJump = (!environment.isMarioOnGround() || environment.isMarioAbleToJump()) ? true : false;
	        System.out.println("  -> canJump=" + canJump);
	        
	        /**
	         5) Mario mode (Mario.MODES)
	         	small: 0
	            large: 1
	            fire: 2
	         */
			int marioMode = environment.getMarioMode();		
			System.out.println("  -> MarioMode=" + marioMode);

			/**
			 * Mario status:
			 * 		Dead: 0  (Mario.STATUS_DEAD)
			 * 		Running: 2 (Mario.STATUS_RUNNING)
			 * 		Win: 1  (Mario.STATUS_WIN)
			 */
			int marioStatus = environment.getMarioStatus();
			System.out.println("  -> MarioStatus=" + marioStatus);
			
			if (marioStatus == Mario.STATUS_DEAD || marioStatus == Mario.STATUS_WIN) {
				System.exit(0);
			}
	    
			// 6) Mario Status

			
			// 7) etc ...
		}
	}
	
	private static boolean isObstacle(byte[][] scene, int x, int y) {
		switch(scene[y][x]) {
			case GeneralizerLevelScene.BRICK:
			case GeneralizerLevelScene.BORDER_CANNOT_PASS_THROUGH:
			case GeneralizerLevelScene.FLOWER_POT_OR_CANNON:
			case GeneralizerLevelScene.LADDER:
			//System.out.println ("OBSTACLE: " + scene[y][x]);
			return true;
		}
		return false;
	}
	
	private boolean isGround(byte[][] scene, int x, int y) {
		return isObstacle(scene, x, y) || scene[y][x] == GeneralizerLevelScene.BORDER_HILL;
	}
}
