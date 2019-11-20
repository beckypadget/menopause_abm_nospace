from mesa import Agent, Model
from timeshuffled import BaseScheduler
from mesa.datacollection import DataCollector

import settings
import random
import uuid
import csv
import pandas as pd
import numpy as np
import math

class Whale(Agent):
    def __init__(self, unique_id, model, age, sex, living, reproductive_status, mother):
        super().__init__(unique_id, model)
        # Assign attributes
        self.age = age # 0 - juvenile; 1 - ya; 2 - oa
        self.sex = sex # 0 - male; 1 - female
        self.living = 1
        self.reproductive_status = reproductive_status # 1 - reproductive; 0 - non-reproductive
        self.mother = mother # mother is a whale
        if self.age == 0:
            self.chance_of_survival = settings.juvenile_survival
        elif self.age > 0:
            self.chance_of_survival = settings.adult_survival

    def step(self):

            # Move to the next age class with a probability given in settings
            if (self.age == 0 and random.random() < settings.probability_ageing):
                self.age = 1

            if (self.age == 1 and random.random() < settings.probability_ageing):
                self.age = 2
            
            # Become post-reproductive, if old, with a probability given in settings
            # if (has a mother, mother was not menopause, is old, is not menopausal, chance)
            if (self.mother is not None and self.mother.reproductive_status == 1 and self.age == 2 and self.reproductive_status != 0 and random.random() < settings.initial_probability_nonreproductive):
                self.reproductive_status = 0
                self.model.pr_whales.append(self)
            # if (has a mother, mother was menopausal, is old, is not menopausal, chance)
            elif (self.mother is not None and self.mother.reproductive_status == 0 and self.age == 2 and self.reproductive_status != 0 and random.random() < settings.inherited_probability_nonreproductive):
                self.reproductive_status = 0
                self.model.pr_whales.append(self)

            # Reproduce with a probability that depends on the presence of maternal relatives
            # if (female, reproductive, chance) 
            if (self.model.step_count < 200): #burn in
                if (self.sex == 1 and self.reproductive_status == 1 and random.random() < settings.initial_chance_of_birth):
                    calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
                    self.model.schedule.add(calf)  

            # # GRANDMOTHER ONLY            
            # elif (self.model.step_count > 100 and self.sex == 1 and self.reproductive_status == 1):
            #     if (self.mother.living == 1 and self.mother.mother.living == 1 and random.random() < (settings.basic_chance_of_birth * settings.reproductive_benefit_of_mother_daughter * settings.reproductive_benefit_of_granny_grandaughter)):
            #         calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #         self.model.schedule.add(calf)
            #     elif (self.mother.living == 1 and self.mother.mother.living == 0 and random.random() < (settings.basic_chance_of_birth * settings.reproductive_benefit_of_mother_daughter)):
            #         calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #         self.model.schedule.add(calf)
            #     elif (self.mother.living == 0 and self.mother.mother.living == 1 and random.random() < (settings.basic_chance_of_birth * settings.reproductive_benefit_of_granny_grandaughter)):
            #         calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #         self.model.schedule.add(calf)
            #     elif(self.mother.living == 0 and self.mother.mother.living == 0 and random.random() < settings.basic_chance_of_birth):
            #         calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #         self.model.schedule.add(calf)

            # # GRANDMOTHER ONLY NEW ##
            # elif (self.model.step_count > 200 and self.sex == 1 and self.reproductive_status == 1):
            #     if (self.mother.living == 1): # if mother is alive
            #         if (self.mother.mother.living == 1): 
            #             if (random.random() < (settings.basic_chance_of_birth * settings.reproductive_benefit_of_mother_daughter * settings.reproductive_benefit_of_granny_grandaughter)): # and grandmother is alive
            #                 calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                 self.model.schedule.add(calf)
            #         elif (self.mother.mother.living == 0):
            #             if (random.random() < (settings.basic_chance_of_birth * settings.reproductive_benefit_of_mother_daughter)):
            #                 calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                 self.model.schedule.add(calf)
            #     elif (self.mother.living == 0):
            #         if (self.mother.mother.living == 1):
            #             if (random.random() < (settings.basic_chance_of_birth * settings.reproductive_benefit_of_granny_grandaughter)):
            #                 calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                 self.model.schedule.add(calf)
            #         elif (self.mother.mother.living == 0):
            #             if (random.random() < settings.basic_chance_of_birth):
            #                 calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                 self.model.schedule.add(calf)

            # # # MALE MATE CHOICE ONLY  ##
            # elif (self.model.step_count > 200 and self.sex == 1 and self.reproductive_status == 1):
            #     if (self.age == 1): 
            #         if (random.random() < (settings.young_chance_of_birth * settings.reproductive_benefit_of_mother_daughter * settings.reproductive_benefit_of_granny_grandaughter)):
            #             calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #             self.model.schedule.add(calf)
            #     elif (self.age == 2):
            #         if (random.random() < (settings.old_chance_of_birth * settings.reproductive_benefit_of_mother_daughter * settings.reproductive_benefit_of_granny_grandaughter)):
            #             calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #             self.model.schedule.add(calf)


            # # FEMALE MATE CHOICE ONLY  ##
            # elif (self.model.step_count > 200 and self.sex == 0 and self.reproductive_status == 1):
            #     if (self.age == 1): 
            #         if (random.random() < settings.young_chance_of_birth):
            #             calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #             self.model.schedule.add(calf)
            #     elif (self.age == 2):
            #         if (random.random() < settings.old_chance_of_birth):
            #             calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #             self.model.schedule.add(calf)

            # GRANDMOTHER PLUS FEMALE MATE CHOICE
                        # ## GRANDMOTHER PLUS MALE MATE CHOICE
            elif (self.model.step_count > 200 and self.sex == 0 and self.reproductive_status == 1):
                if (self.mother.living == 1): # if mother is alive
                    if (self.mother.mother.living == 1): # and grandmother is alive
                        if (self.age == 1): 
                            if (random.random() < (settings.young_chance_of_birth * settings.reproductive_benefit_of_mother_daughter * settings.reproductive_benefit_of_granny_grandaughter)):
                                calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
                                self.model.schedule.add(calf)
                        elif (self.age == 2):
                            if (random.random() < (settings.old_chance_of_birth * settings.reproductive_benefit_of_mother_daughter * settings.reproductive_benefit_of_granny_grandaughter)):
                                calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
                                self.model.schedule.add(calf)
                    elif (self.mother.mother.living == 0): # and grandmother is not alive
                        if (self.age == 1): 
                            if (random.random() < (settings.young_chance_of_birth * settings.reproductive_benefit_of_mother_daughter)):
                                calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
                                self.model.schedule.add(calf)
                        elif (self.age == 2): 
                            if (random.random() < (settings.old_chance_of_birth * settings.reproductive_benefit_of_mother_daughter)):
                                calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
                                self.model.schedule.add(calf)

                elif (self.mother.living == 0): # is mother is dead
                    if (self.mother.mother.living == 1): # and grandmother is alive
                        if(self.age == 1):
                            if (random.random() < (settings.young_chance_of_birth * settings.reproductive_benefit_of_granny_grandaughter)):
                                calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
                                self.model.schedule.add(calf)
                        elif (self.age == 2):
                            if (random.random() < (settings.old_chance_of_birth * settings.reproductive_benefit_of_granny_grandaughter)):
                                calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
                                self.model.schedule.add(calf)
                    elif (self.mother.mother.living == 0): # and grandmother is not alive
                        if (self.age == 1):
                            if (random.random() < settings.young_chance_of_birth):
                                calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
                                self.model.schedule.add(calf)
                        elif (self.age == 2):
                            if (random.random() < settings.old_chance_of_birth):
                                calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
                                self.model.schedule.add(calf)

            # # ## GRANDMOTHER PLUS MALE MATE CHOICE
            # elif (self.model.step_count > 200 and self.sex == 1 and self.reproductive_status == 1):
            #     if (self.mother.living == 1): # if mother is alive
            #         if (self.mother.mother.living == 1): # and grandmother is alive
            #             if (self.age == 1): 
            #                 if (random.random() < (settings.young_chance_of_birth * settings.reproductive_benefit_of_mother_daughter * settings.reproductive_benefit_of_granny_grandaughter)):
            #                     calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                     self.model.schedule.add(calf)
            #             elif (self.age == 2):
            #                 if (random.random() < (settings.old_chance_of_birth * settings.reproductive_benefit_of_mother_daughter * settings.reproductive_benefit_of_granny_grandaughter)):
            #                     calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                     self.model.schedule.add(calf)
            #         elif (self.mother.mother.living == 0): # and grandmother is not alive
            #             if (self.age == 1): 
            #                 if (random.random() < (settings.young_chance_of_birth * settings.reproductive_benefit_of_mother_daughter)):
            #                     calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                     self.model.schedule.add(calf)
            #             elif (self.age == 2): 
            #                 if (random.random() < (settings.old_chance_of_birth * settings.reproductive_benefit_of_mother_daughter)):
            #                     calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                     self.model.schedule.add(calf)

            #     elif (self.mother.living == 0): # is mother is dead
            #         if (self.mother.mother.living == 1): # and grandmother is alive
            #             if(self.age == 1):
            #                 if (random.random() < (settings.young_chance_of_birth * settings.reproductive_benefit_of_granny_grandaughter)):
            #                     calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                     self.model.schedule.add(calf)
            #             elif (self.age == 2):
            #                 if (random.random() < (settings.old_chance_of_birth * settings.reproductive_benefit_of_granny_grandaughter)):
            #                     calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                     self.model.schedule.add(calf)
            #         elif (self.mother.mother.living == 0): # and grandmother is not alive
            #             if (self.age == 1):
            #                 if (random.random() < settings.young_chance_of_birth):
            #                     calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                     self.model.schedule.add(calf)
            #             elif (self.age == 2):
            #                 if (random.random() < settings.old_chance_of_birth):
            #                     calf = Whale(self.model.next_id(), self.model, 0, int(bool(random.getrandbits(1))), 1, 1, self)
            #                     self.model.schedule.add(calf)


            # Die with a probability given in settings
            if (random.random() > self.chance_of_survival + (1 / (1 * self.model.schedule.get_agent_count()))):
                if self in self.model.pr_whales:
                    self.model.pr_whales.remove(self)
                self.model.schedule.remove(self)
                self.living = 0



class WhaleModel(Model):
    def __init__(self, N, run_number):
        super().__init__()
        self.run_number = run_number
        self.num_agents = N
        self.schedule = BaseScheduler(self)
        self.step_count = 0
        self.pr_whales = []
        self.data = {'step': [], 'population': [], 'prop': [], 'juvenile': [], 'young_adult': [], 'old_adult': [], 'run':[]}
        self.field_names = ['step', 'population', 'prop', 'juvenile', 'young_adult', 'old_adult', 'run']
        # self.mate_choice = mate_choice
        # self.grandmother_effect = grandmother_effect

        # Create agents
        matriarch = Whale("matriarch", self, random.choice([1,2]), int(bool(random.getrandbits(1))), 1, 1, None)

        for i in range(self.num_agents):
            new_whale = Whale(i, self, random.choice([0,1,2]), int(bool(random.getrandbits(1))), 1, 1, matriarch)
            self.schedule.add(new_whale)

    def step(self):
        # Move model on one step
        self.schedule.step()
        self.step_count += 1

        self.data['step'].append(self.step_count)
        self.data['population'].append(self.schedule.get_agent_count())
        self.data['prop'].append(self.get_proportion_postreproductive())
        self.data['juvenile'].append(self.get_juv_whales())
        self.data['young_adult'].append(self.get_young_whales())
        self.data['old_adult'].append(self.get_old_whales())
        self.data['run'].append(self.run_number)

    def write_data(self, filename):
        data_frame = pd.DataFrame(self.data, columns = ['step','population', 'prop', 'juvenile', 'young_adult', 'old_adult', 'run'])
        data_frame.to_csv('{}.csv'.format(filename), index = False)

    def get_proportion_postreproductive(self):
        if self.schedule.get_agent_count() > 0:
            proportion_postreproductive = len([agent for agent in self.schedule.agents if agent.reproductive_status == 0]) / self.schedule.get_agent_count()
        else:
            proportion_postreproductive = "NA"
        return proportion_postreproductive

    def get_juv_whales(self):
        if self.schedule.get_agent_count() > 0:
            proportion_juv = len([agent for agent in self.schedule.agents if agent.age == 0]) / self.schedule.get_agent_count()
        else:
            proportion_juv = "NA"
        return proportion_juv

    def get_young_whales(self):
        if self.schedule.get_agent_count() > 0:
            proportion_young = len([agent for agent in self.schedule.agents if agent.age == 1]) / self.schedule.get_agent_count()
        else:
            proportion_young = "NA"
        return proportion_young

    def get_old_whales(self):
        if self.schedule.get_agent_count() > 0:
            proportion_old = len([agent for agent in self.schedule.agents if agent.age == 2]) / self.schedule.get_agent_count()
        else:
            proportion_old = "NA"
        return proportion_old