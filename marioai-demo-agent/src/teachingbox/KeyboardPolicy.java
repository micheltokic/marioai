package teachingbox;

import java.io.IOException;

import org.hswgt.teachingbox.core.rl.datastructures.ActionSet;
import org.hswgt.teachingbox.core.rl.env.Action;
import org.hswgt.teachingbox.core.rl.env.State;
import org.hswgt.teachingbox.core.rl.policy.Policy;
import org.jline.terminal.Terminal;
import org.jline.terminal.TerminalBuilder;
import org.jline.utils.NonBlockingReader;

public class KeyboardPolicy implements Policy {

	/**
	 * This class reads in Actions from the keyboard
	 */
	private static final long serialVersionUID = 7265857397948329280L;
	private ActionSet ACTION_SET;

	public KeyboardPolicy (ActionSet actions) {
		this.ACTION_SET = actions;
	}
	
	
	@Override
	public Action getAction(State state) {
		
		/**
		 * TODO: read in action from keyboard and fetch corresponding Action from the ActionSet
		 */
		int actionId = 0;
		// read in actionId from keyboard (cf. example in main() function)
		
		Action a = ACTION_SET.get(actionId);
		
		return a;
	}

	@Override
	public Action getBestAction(State state) {
		return this.getAction(state);
	}

	@Override
	public double getProbability(State state, Action action) {
		// NOT REQUIRED 
		return 0;
	}

	
	public static void main(String[] args) {
		
		/**
		 * Example for reading in single characters from the console 
		 * Runs on Cygwin in Windows. 
		 * 
		 * CMD call: java -cp mario-0.0.1-SNAPSHOT.jar mario.teachingbox.KeyboardPolicy
		 */
		Terminal terminal;
		try {
			terminal = TerminalBuilder.builder()
				    .jna(true)
				    .system(true)
				    .build();

			// raw mode means we get keypresses rather than line buffered input
			terminal.enterRawMode();
			NonBlockingReader reader = terminal .reader();
			//...
			for (int i=0; i<10; i++) {
				System.out.print("Press key: ");
				int read = reader.read();
				System.out.println("  => You typed: " + (char)read + " => "+ read + ":int");
			}
			//....
			reader.close();
			terminal.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
