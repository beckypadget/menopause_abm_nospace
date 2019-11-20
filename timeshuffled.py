# -*- coding: utf-8 -*-

from collections import OrderedDict
import random

class BaseScheduler:
    """ Simplest scheduler; activates agents one at a time, in the order
    they were added.

    Assumes that each agent added has a *step* method which takes no arguments.

    (This is explicitly meant to replicate the scheduler in MASON).

    """
    def __init__(self, model):
        """ Create a new, empty BaseScheduler. """
        self.model = model
        self.steps = 0
        self.time = 0
        self._agents = OrderedDict()

    def add(self, agent):
        """ Add an Agent object to the schedule.

        Args:
            agent: An Agent to be added to the schedule. NOTE: The agent must
            have a step() method.

        """
        self._agents[agent.unique_id] = agent

    def remove(self, agent):
        """ Remove all instances of a given agent from the schedule.

        Args:
            agent: An agent object.

        """
        del self._agents[agent.unique_id]


    # def step(self):
    #     """ Determine the next event then assign a random whale to do it. """
    #     # Probabilities
    #     age = 
    #     reproduce =
    #     die =
    #     menopause_mutation = 0.05
    #     inherited_menopause = 

    #     # Numbers of each sub-population
    #     young_female = 
    #     old_female = 
    #     young_male = 
    #     old_male = 
    #     pr_female = 0

    def step(self):
        """ Execute the step of all the agents, one at a time. """
        for agent in self.agent_buffer(shuffled=True):
            agent.step()
        self.steps += 1
        self.time += 1

    def get_agent_count(self):
        """ Returns the current number of agents in the queue. """
        return len(self._agents.keys())

    @property
    def agents(self):
        return list(self._agents.values())

    def agent_buffer(self, shuffled=False):
        """ Simple generator that yields the agents while letting the user
        remove and/or add agents during stepping.

        """
        agent_keys = list(self._agents.keys())
        if shuffled:
            random.shuffle(agent_keys)

        for key in agent_keys:
            if key in self._agents:
                yield self._agents[key]


"""
mymesamod Time Module
================

Objects for handling the time component of a model. In particular, this module
contains Schedulers, which handle agent activation. A Scheduler is an object
which controls when agents are called upon to act, and when.

The activation order can have a serious impact on model behavior, so it's
important to specify it explicitly. Example simple activation regimes include
activating all agents in the same order every step, shuffling the activation
order every time, activating each agent *on average* once per step, and more.

Key concepts:
    Step: Many models advance in 'steps'. A step may involve the activation of
    all agents, or a random (or selected) subset of them. Each agent in turn
    may have their own step() method.

    Time: Some models may simulate a continuous 'clock' instead of discrete
    steps. However, by default, the Time is equal to the number of steps the
    model has taken.


TODO: Have the schedulers use the model's randomizer, to keep random number
seeds consistent and allow for replication.

"""
