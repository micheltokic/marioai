package apidemo;


import ch.idsia.agents.Agent;
import ch.idsia.agents.controllers.BasicMarioAIAgent;

import ch.idsia.benchmark.mario.environments.Environment;


/**
 * This class is required by the MarioAI-Engine. It is NOT a Teachingbox Agent!
 * @author Michel Tokic
 *
 */


public class ApiAgent extends BasicMarioAIAgent implements Agent {

	public ApiAgent()
	{
	    super("TeachingBoxAgent");
	    reset();
	}

	private boolean[] action = null;

	public void reset()
	{
		action = new boolean[Environment.numberOfKeys];
	}
	
	public void setAction(boolean[] action)
	{
		this.action = action;
	}

	public boolean[] getAction()
	{
	    return this.action;
	}
	
}

