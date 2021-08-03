from os import error
from qlearner import QLearner
import numpy as np
from gym_setup import Env

n_episodes = 5000
alpha = 0.1
gamma = 0.99
lmbda = 0.75
epsilon_start = 0.5
epsilon_end = 0.01
epsilon_decay_length = n_episodes / 2
decay_step = (epsilon_end - epsilon_start) / epsilon_decay_length

#level = 'oneCliffLevel'
#path = gym_marioai.levels.one_cliff_level
#rf_width = 20
#rf_height = 10

# can be finetuned
# (TODO these are working parameters, change the initial values for the exercise)
# the trace parameter is the number of consecutive observations that are used as 
# state information (k-th order history)
trace = 2

def train(env, agent):
    try:
        all_rewards = np.zeros([n_episodes])
        all_wins = np.zeros([n_episodes])
        all_steps = np.zeros([n_episodes])
        all_jumps = np.zeros([n_episodes])
        
        for e in range(n_episodes):
            done = False
            info = {}
            total_reward = 0
            steps = 0
            epsilon = max(epsilon_end, epsilon_start + e * decay_step)
            
            state = env.reset()
            action = agent.choose_action(state, epsilon)
            
            while not done:
                next_state, reward, done, info = env.step(action)
                total_reward += reward
                next_action = agent.choose_action(next_state, epsilon)
                agent.learn(state, action, reward, next_state, next_action)
                
                state, action = next_state, next_action
                steps += 1
                
            # store statistics for later use
            all_rewards[e] = total_reward
            all_wins[e] = 1 if info['win'] else 0
            all_steps[e] = info['steps']
            all_jumps[e] = info['cliff_jumps']

            if e % 100 == 99:
                # print training statistics of the last 100 episodes
                avg_reward = all_rewards[e-99:e+1].mean()
                avg_wins = all_wins[e-99:e+1].mean()
                avg_steps = all_steps[e-99:e+1].mean()
                avg_jumps = all_jumps[e-99:e+1].mean()
                
                print(f'Episode: {e+1} Eps: {epsilon:.3f}', f'Avg Reward: {avg_reward:>4.2f}',
                    f'Avg steps: {avg_steps:>4.2f}', f'Win% : {avg_wins:3.2f}',
                    f'Cliff jumps: {avg_jumps:.1f}', f'States seen: {agent.Q.num_states}    ', end='\r')
        print()        
        return all_rewards, all_wins, all_steps, all_jumps
    except KeyboardInterrupt:
        agent.save('exercise_2/data/trained')
        pass




env = Env(visible=False)
env = env.get_env()

agent = QLearner(env, alpha, gamma, lmbda)
try:
    agent.load('exercise_2/data/userdata')
except error as e:
    print(e)

rewards, wins, steps, jumps = train(env, agent)
agent.save('exercise_2/data/trained')
