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
	self.gamma = 1
	self.epsilon = 0.5
	self.alpha = 1
	self.QTable = {}

    def reset(self, destination=None):
        self.planner.route_to(destination)
        
	# TODO: Prepare for a new trip; reset any variables here, if required
	self.gamma = 1
	self.epsilon = 0.01
	self.alpha = 1

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self) # light, oncoming, left, right
        deadline = self.env.get_deadline(self)
        
	# TODO: Update state
        self.state = (inputs['light'], inputs['oncoming'], inputs['left'], inputs['right'], self.next_waypoint)
	
	if self.state not in self.QTable:
		self.QTable[self.state] = {None: 10, 'left': 10, 'right': 10, 'forward': 10}
	
	# TODO: Select action according to your policy 
	if random.random() < self.epsilon:
		action = random.choice([None, 'left', 'right', 'forward'])
	else:
		action = max(zip(self.QTable[self.state].values(), self.QTable[self.state].keys()))[1]
        
	# Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
	q_prime = max(zip(self.QTable[self.state].values(), self.QTable[self.state].keys()))[0]
	old_q = self.QTable[self.state][action]
	self.QTable[self.state][action] = old_q + self.alpha*(reward + self.gamma*q_prime - old_q) 
	print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
