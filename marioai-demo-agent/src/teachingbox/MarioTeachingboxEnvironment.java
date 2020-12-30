package teachingbox;

import java.util.LinkedHashMap;
import java.util.Map.Entry;

import org.hswgt.teachingbox.core.rl.datastructures.ActionSet;
import org.hswgt.teachingbox.core.rl.env.Action;
import org.hswgt.teachingbox.core.rl.env.Environment;
import org.hswgt.teachingbox.core.rl.env.State;
import ch.idsia.benchmark.mario.engine.sprites.Mario;
import ch.idsia.benchmark.mario.engine.sprites.Sprite;
import ch.idsia.benchmark.mario.environments.MarioEnvironment;
import ch.idsia.tools.MarioAIOptions;
import apidemo.ApiAgent;


/**
 * This Teachingbox environment interfaces the MarioAI engine
 * 
 * @author Michel Tokic
 *
 */

public class MarioTeachingboxEnvironment implements Environment {

	
	private static final long serialVersionUID = 7139180076433799346L;

	/**
	 *  construct ACTION_SET (required by Policy/Q-Function)
	 */
	public static final ActionSet ACTION_SET = new ActionSet();	
	protected static LinkedHashMap <Action, String> ACTIONS = new LinkedHashMap<Action, String>();
	protected static LinkedHashMap <String, Action> ACTION_MAP = new LinkedHashMap<String,Action>();
	static {
		//ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_LEFT)}), "LEFT");  // -> SPEED_LEFT
		//ACTIONS.put(new Action(new double[]{(double)(1 << Mario.KEY_RIGHT)}), "RIGHT");// -> SPEED_RIGHT
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
	
	private State currentState  = new State(new double[] {0});

	private ApiAgent apiAgent = new ApiAgent();

	private float marioXold=0;

	private static final MarioEnvironment environment = MarioEnvironment.getInstance();
	
	
	
	@Override
	public double doAction(Action action) {
		
		/** 
		 *  Perform Action in MarioAI-Engine
		 */
	    boolean[] marioAiAction = new boolean[ch.idsia.benchmark.mario.environments.Environment.numberOfKeys];
	    
	    for (int i=0; i<ch.idsia.benchmark.mario.environments.Environment.numberOfKeys; i++) {
			marioAiAction[i] = ((int)action.get(0) & (1<<i)) > 0 ? true : false;
		}
		apiAgent.setAction(marioAiAction);
		environment.performAction(apiAgent.getAction());
		environment.tick();
        apiAgent.integrateObservation(environment);
        
        
		/**
		 *  TODO Compute reward
		 *     Important: calling MarioEnvironment.getIntermediateReward() can be misleading, because
		 *     we might have too less features that explain the reward, thus introducing noisy rewards
		 */
		double reward = 0; // <-- compute reward from state features, e.g. killed enemies, deltaX, jump over gap, ...   

		// easiest reward: learn to walk from left to right by rewarding movements in X direction
		float[] pos = environment.getMarioFloatPos();
        float marioX = pos[0];
        float marioY = pos[1];
        float deltaX = marioX - marioXold;
        System.out.println("  -> MarioPos: x=" + marioX + ", y=" + marioY + ", oldX=" + marioXold + " => reward=" + deltaX);
        reward = deltaX;
        marioXold = marioX;
        
        this.currentState = new State (getStateFeatures());
		
		// return reward
		return reward;
	}

	@Override
	public State getState() {
		return this.currentState;
	}

	@Override
	public boolean isTerminalState() {
		 // check MarioEnvironment if Mario has been killed or reached the goal
		return environment.getMarioStatus() != 2 ? true : false;
	}

	@Override
	public void initRandom() {
		/**
		 * TODO: 1) Initialize MarioAI environment with desired parameters
		 */
		// setup level options
		MarioAIOptions marioAIOptions = new MarioAIOptions("");
		marioAIOptions.setFlatLevel(false);
		marioAIOptions.setBlocksCount(true);
		marioAIOptions.setCoinsCount(true);
		marioAIOptions.setLevelRandSeed(1000); // comment out for random levels
		marioAIOptions.setVisualization(true); // false: no visualization => faster learning
		marioAIOptions.setGapsCount(false);
		marioAIOptions.setMarioMode(2);
		marioAIOptions.setLevelLength(80);
		marioAIOptions.setCannonsCount(false);
		marioAIOptions.setTimeLimit(100);
		marioAIOptions.setDeadEndsCount(false);
		marioAIOptions.setTubesCount(false);
		marioAIOptions.setLevelDifficulty(0);
		marioAIOptions.setReceptiveFieldVisualized(true);
		// -srf on  => "show receptive field"
		// -vh 480  => height: 480 pixel
		// -vw 640  => width:  640 pixel
		marioAIOptions.setArgs(" -srf on -vh 360 -vw 640 "); // cf. CmdLineOptions.pdf for more parameters 
		
		// configure Agent
		// setup engine 
		marioAIOptions.setAgent(apiAgent); 
		apiAgent.setObservationDetails(environment.getReceptiveFieldWidth(),
	    		environment.getReceptiveFieldHeight(),
	    		environment.getMarioEgoPos()[0],
	    		environment.getMarioEgoPos()[1]);
		
		// reset environment
		environment.reset(marioAIOptions);
		marioAIOptions.printOptions(true);
		
		this.currentState = new State (getStateFeatures());
	}
	
	/**
	 * TODO: construct state features from current observation (possible also old observations)
	 */
	private double[] getStateFeatures() {
		
		// => inspect receptive field for enemies / mario is stuck / gaps ... 
		byte[][] scene = environment.getMergedObservationZZ(1, 1);
		System.out.println("scene.maxY=" + scene.length);
		System.out.println("scene.maxX=" + scene[0].length);
		
		boolean goombaFound = false;
		for (int x=0; x<scene[0].length; x++) {
		   for (int y=0; y<scene.length; y++) {
			   if (scene[y][x] == Sprite.KIND_GOOMBA) {
				   System.out.println("GOOMBA AT x=" + x + "y=" + y);
				   goombaFound = true;
				   // => do something reasonable with this information
			   }
		   }
		}
		if (goombaFound) {
			float[] pos = environment.getMarioFloatPos();
		    float marioX = pos[0];
		    float marioY = pos[1];
		
		    System.out.println("marioX=" + marioX + ", marioY=" + marioY);
		    System.out.println("DEBUG GOOMBAS");
		}
		
		// TODO: construct reasonable state features ... 
		// isObstacle(scene, x, y)
        // isGround (scene, x, y)
        // if (scene[y][x] == Sprite.KIND_GOOMBA ||
		//	  scene[y][x] == Sprite.KIND_SPIKY /* .... */) {

		return new double[] {0}; 
	}

	@Override
	public void init(State state) {
		this.initRandom();
	}
}
