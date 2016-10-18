import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import random

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        
	# TODO: Initialize any additional variables here
	self.gamma = 0
	self.epsilon = 0.1
	self.alpha = 1
	self.QTable = {}

    def reset(self, destination=None):
        self.planner.route_to(destination)
        
	# TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self) # light, oncoming, left, right
        deadline = self.env.get_deadline(self)
        
	# TODO: Update state
	self.state = (inputs['light'], inputs['oncoming'], inputs['left'], self.next_waypoint)
	if self.state not in self.QTable:
		self.QTable[self.state] = {None: 12, 'left': 12, 'right': 12, 'forward': 12}
	
	# TODO: Select action according to your policy 
	actions = self.QTable[self.state].keys()
	values = self.QTable[self.state].values()	
	max_value = max(values)
	best_actions = [action for action in self.QTable[self.state].keys() if self.QTable[self.state][action] == max_value]	
	
	if random.random() < self.epsilon:
		#Static epsilon method adds a scaled value randomly to the expected outcome and picks the max 
		#See https://studywolf.wordpress.com/2012/11/25/reinforcement-learning-q-learning-and-exploration/
		random_values = [0.1*(max_value+0.25), 0.2*(max_value+0.25), 0.3*(max_value+0.25), 0.4*(max_value+0.25)]
		random.shuffle(random_values)
		new_values = [v+random_values.pop() for v in values]
		max_v = max(new_values)
		index = new_values.index(max_v)
		action = actions[index]
	else:
		action = random.choice(best_actions)
        
	# Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        new_inputs = self.env.sense(self) 
        new_waypoint = self.planner.next_waypoint() 
	next_state = (new_inputs['light'], new_inputs['oncoming'], new_inputs['left'], new_waypoint) 
	q_prime = max(self.QTable[next_state].values())
	old_q = self.QTable[self.state][action]
	self.QTable[self.state][action] = old_q + self.alpha*(reward + self.gamma*q_prime - old_q) 
	#print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.1, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
