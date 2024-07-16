# -- coding: utf-8 --**
import pdb
import time
import mesa
from utils import get_completion_from_messages, get_completion_from_messages_json, probability_threshold
import logging
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
import json
from prompt import *

def get_summary_long(long_memory, short_memory):
    user_msg = long_memory_prompt.format(long_memory=long_memory, short_memory=short_memory)

    msg = [{"role": "user", "content": user_msg}]

    get_summary = get_completion_from_messages(msg, temperature=1)

    return get_summary

def get_summary_short(opinions,topic):
    opinions_text = "\n".join(f"One people think: {opinion}" for opinion in opinions)

    user_msg = reflecting_prompt.format(opinions=opinions_text,topic=topic)

    msg = [{"role": "user", "content": user_msg}]

    get_summary = get_completion_from_messages(msg, temperature=0.5)

    return get_summary


class Citizen(mesa.Agent):
    '''
    Define who a citizen is:
    unique_id: assigns ID to agent
    name: name of the agent
    age: age of the agent
    traits: big 5 traits of the agent
    health_condition: flag to say if Susceptible or Infected or Recovered
    day_infected: agent attribute to count the number of days agent spends infected
    width, height: dimensions of world
    '''

    def __init__(self, model, unique_id, name, age, traits, qualification, health_condition, opinion, topic):
                
        super().__init__(unique_id,model) #Inherit mesa.Agent class attributes (model is mesa.Model)
        #Persona
        self.name = name
        self.age = age
        self.opinion=opinion
        self.traits=traits
        self.qualification=qualification
        self.topic=topic
        self.opinions = []
        self.beliefs = []
        self.long_opinion_memory = ''
        self.long_memory_full = []
        self.short_opinion_memory = []
        self.reasonings = []
        self.contact_ids = []

        #Health Initialization of Agent
        self.health_condition=health_condition

        #Contact Rate  
        self.agent_interaction=[]

        #Reasoning tracking
        self.persona = {"name":name, "age":age, "traits":traits}

        self.initial_belief, self.initial_reasoning = self.initial_opinion_belief()
        self.opinions.append(self.opinion)
        self.beliefs.append(self.initial_belief)
        self.reasonings.append(self.initial_reasoning)

    ########################################
    #          Initial Opinion             #
    ########################################
    def initial_opinion_belief(self):
        if self.health_condition == 'Infected':
            belief = 1
        else:
            belief = 0

        reasoning = 'initial_reasoning'

        return belief, reasoning


    ################################################################################
    #                       Meet_interact_infect functions                         #
    ################################################################################ 

    def interact(self):
        ''' 
        Step 1. Run infection for each agent_interaction
        Step 2. Reset agent_interaction for next day
        Used in self.step()
        '''
        
        others_opinions = []
        contact_id = []
        for agent in self.agent_interaction:
            contact_id.append(agent.unique_id)
            agent_latest_opinion = agent.opinions[-1]
            others_opinions.append(agent_latest_opinion)
        self.short_opinion_memory.append(others_opinions)
        self.contact_ids.append(contact_id)
        
        opinion_short_summary = get_summary_short(others_opinions,topic=self.topic)

        long_mem = get_summary_long(self.long_opinion_memory, opinion_short_summary)

        user_msg = update_opinion_prompt.format(agent_persona=self.traits,
                                                agent_qualification=self.qualification,
                                                agent_name=self.name,
                                                long_mem=long_mem,
                                                topic=self.topic,
                                                opinion=self.opinion)
        
        self.opinion, self.belief, self.reasoning = self.response_and_belief(user_msg)
        self.opinions.append(self.opinion)
        self.beliefs.append(self.belief)
        self.reasonings.append(self.reasoning)
        print(str(self.unique_id))
        print(self.reasoning)
        print(str(self.belief))

        self.long_opinion_memory = long_mem
        self.long_memory_full.append(self.long_opinion_memory)
        #Reset Agent Interaction list
        self.agent_interaction=[]
        self.get_health()
    ########################################
    #               Infect                 #
    ########################################
        
    def response_and_belief(self, user_msg):

        msg = [{"role": "user", "content": user_msg}]
        response_json = get_completion_from_messages_json(msg, temperature=1)
        output = json.loads(response_json)
        tweet = output['tweet']
        belief = output['belief']
        reasoning = output['reasoning']
        belief = int(belief)
        return tweet, belief, reasoning



    def get_health(self):
        if self.health_condition=='Infected' and self.belief == 0:
            self.health_condition='to_be_recover'
        elif self.health_condition!='Infected' and self.belief == 1 :
            self.health_condition='to_be_infected'
        else:
            pass



    ################################################################################
    #                              step functions                                  #
    ################################################################################
  

    def step(self):
        '''
        Step function for agent
        '''
        self.interact()
