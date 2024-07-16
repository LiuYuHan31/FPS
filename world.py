import mesa
from citizen import Citizen
from tqdm import tqdm
from datetime import datetime, timedelta
from utils import generate_names,generate_big5_traits, generate_qualifications, factorize, update_day, clear_cache
import random
import pickle
from prompt import *

# functions for mesa.DataCollector in World class
def compute_num_susceptible(model):
    '''
    Computers number of susceptible agents for data frame
    '''
    return sum([1 for a in model.schedule.agents if a.health_condition == "Susceptible"])


def compute_num_infected(model):
    '''
    Computers number of infected agents for data frame
    '''
    return sum([1 for a in model.schedule.agents if a.health_condition == "Infected"])


def compute_num_recovered(model):
    '''
    Computers number of recovered agents for data frame
    '''
    return sum([1 for a in model.schedule.agents if a.health_condition == "Recovered"])


def compute_num_on_grid(model):
    '''
    Computers number of agents on the grid
    '''
    return sum([1 for a in model.schedule.agents if a.location == "grid"])


def compute_num_at_home(model):
    '''
    Computers number of agents at home
    '''
    return sum([1 for a in model.schedule.agents if a.location == "home"])


class World(mesa.Model):
    '''
    The world where Citizens exist
    '''
    def __init__(self, args, initial_healthy=2, initial_infected=1, contact_rate=5):
        
        ########################################
        #     Intialization of the world       #
        ########################################
    
        #Agent initialization
        self.initial_healthy=initial_healthy
        self.initial_infected=initial_infected
        self.population=initial_healthy+initial_infected
        self.step_count = args.no_days
        self.offset = 0 #Offset for checkpoint load
        self.name = args.name
        self.topic="The central bank will implement new regulations on large deposits, and all large deposits must present specific proof materials."

        #Important infection variables
        self.total_contact_rates = 0
        self.track_contact_rate = [0]
        self.list_new_infected_cases = [0]
        self.list_new_susceptible_cases = [0]
        self.daily_new_infected_cases = initial_infected
        self.daily_new_susceptible_cases = initial_healthy
        self.infected = initial_infected
        self.susceptible = initial_healthy
        self.current_date = datetime(2020, 3, 3)
        self.contact_rate= args.contact_rate   
        self.max_potential_interactions=0
        #Initialize Schedule
        self.schedule = mesa.time.RandomActivation(self)  

        #Initiate data collector
        self.datacollector = mesa.DataCollector(
            model_reporters={"Susceptible": compute_num_susceptible,
                            "Infected": compute_num_infected,
                            "Recovered": compute_num_recovered,
                            })
        

        ########################################
        #Assigning properties to all 100 agents#
        ########################################

        #IDs for agents
        agent_id = 0 

        #generates list of random names out of the 200 most common names in the US
        names = generate_names(self.population, self.population*2)
        traits = generate_big5_traits(self.population)
        qualifications = generate_qualifications(self.population)

        #for loop to initialize each agents
        for i in range(self.population):

            #Creates healthy agents
            if i+1<=(self.initial_healthy):
                health_condition="Susceptible"
                opinion=random.choice(finance_sentence_susceptible)

            #Creates infected, unhealthy agent(s)
            else:
                health_condition = "Infected"
                opinion=random.choice(finance_sentence_infeted)


            #create instances of the Citizen class
            citizen = Citizen(model=self,
                              unique_id=agent_id, name=names[i], age=random.randrange(18,65),
                              traits=traits[i], opinion=opinion,
                              qualification=qualifications[i],
                              health_condition=health_condition,
                              topic=self.topic
                              )  
            # add agents to the scheduler
            self.schedule.add(citizen)
            # Updates to new agent ID
            agent_id += 1 


    def decide_agent_interactions(self):
        '''
        Decides interaction partners for each agent
        '''
        self.max_potential_interactions = self.contact_rate
        for agent in self.schedule.agents:
            potential_interactions = [a for a in self.schedule.agents if a is not agent]  
            random.shuffle(potential_interactions) 
            potential_interactions=potential_interactions[:self.max_potential_interactions]  
            for other_agent in potential_interactions:
                agent.agent_interaction.append(other_agent)    

    def step(self):
        '''
        Model time step
        '''
        
        self.decide_agent_interactions()  
       
        for agent in self.schedule.agents: #track global contact rate
            self.total_contact_rates += len(agent.agent_interaction)
        self.track_contact_rate.append(self.total_contact_rates)
        self.total_contact_rates = 0

        # call the step function of every agent
        self.schedule.step()

        #Update day of each agent
        for agent in self.schedule.agents:
            update_day(agent)


    #Function to actually run the model
    def run_model(self, checkpoint_path, offset=0):
        self.offset = offset
        end_program=0
        for i in tqdm(range(self.offset,self.step_count)):
            #collect model level data
            self.datacollector.collect(self)

            #Model steps
            self.step()  

            #collect all new cases from one day
            self.list_new_infected_cases.append(self.daily_new_infected_cases)
            self.list_new_susceptible_cases.append(self.daily_new_susceptible_cases)
            #set daily new case to 0 again
            self.daily_new_infected_cases = 0
            self.daily_new_susceptible_cases = 0

            #Print statements
            print(f"At the end of {self.current_date.date()}")
            print(f"Total Pop: {self.population}\t New Infected Cases: {self.list_new_infected_cases} \t New Susceptible_Cases: {self.list_new_susceptible_cases}")
            print (f"Currently Infected: {self.infected}")

            """
            early stopping condition: if there are no more infected agents left, 
            run for two more time steps, save the model and then end program
            """
            if self.infected==0:
                end_program+=1
            if end_program == 2:
                path = checkpoint_path + f"/{self.name}-final_early.pkl"
                self.save_checkpoint(file_path = path)
                break

            self.current_date += timedelta(days=1)
            path = checkpoint_path+f"/{self.name}-{i+1}.pkl"
            self.save_checkpoint(file_path = path)
            clear_cache()


    #saves checkpoint to specified file path
    def save_checkpoint(self, file_path):
        with open(file_path,"wb") as file:
            pickle.dump(self, file)
    
    @staticmethod
    def load_checkpoint(file_path):
        with open(file_path,"rb") as file:
            return pickle.load(file)
