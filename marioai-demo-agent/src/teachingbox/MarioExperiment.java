package teachingbox;

import org.hswgt.teachingbox.core.rl.agent.Agent;
import org.hswgt.teachingbox.core.rl.experiment.Experiment;
import org.hswgt.teachingbox.core.rl.learner.TabularQLearner;
import org.hswgt.teachingbox.core.rl.policy.EpsilonGreedyPolicy;
import org.hswgt.teachingbox.core.rl.policy.Policy;
import org.hswgt.teachingbox.core.rl.tabular.HashQFunction;
import org.hswgt.teachingbox.core.rl.tools.ObjectSerializer;
import org.hswgt.teachingbox.core.rl.valuefunctions.QFunction;


public class MarioExperiment {

	public static void main(String[] args) {
		/**
		 *  TODO:  Exercise 1:
		 *  Improve MarioTeachingboxEnvironment.doAction() in order that Mario gets enough features that help reaching the goal 
		 */
		MarioTeachingboxEnvironment env = new MarioTeachingboxEnvironment();
		HashQFunction Q = new HashQFunction (0, MarioTeachingboxEnvironment.ACTION_SET);
		Policy pi = new EpsilonGreedyPolicy(Q, MarioTeachingboxEnvironment.ACTION_SET, 0.1);
		Agent agent = new Agent (pi);

		// configure learner
		TabularQLearner learner = new TabularQLearner(Q);
		// TODO: replace Q-learning with SARSA once good meta parameters were found. Is there any difference?
		//TabularSarsaLearner learner = new TabularSarsaLearner(Q);
		learner.setAlpha(0.1);
		learner.setGamma(0.95);
		agent.addObserver(learner);
		
		// configure experiment
		Experiment experiment = new Experiment (agent, env, 100, 1000);
		experiment.run();
		
		
		// ... siehe de.lmu.arl.crawler.Main
		
		
		/**
		 * Exercise 2:
		 */
		// use keyboard policy
		//Policy pi = new KeyboardPolicy (Q);
		//...
		
		// memorize Q-function to disk
		//ObjectSerializer.save("Q-function.dat", Q);
		
		// 
		// load Q-function from disk and apply Greedy policy on learned Q-function
		//ObjectSerializer.load("Q-function.dat");
		
	}
}
