from turtle import pd
import numpy as np
import matplotlib.pyplot as plt
import  pandas as pd
# Import the MarkovChain class from markovchain.py
from markovchain import MarkovChain
import random as random

# P = np.array([[0.8, 0.2], [0.1, 0.9]]) # Transition matrix
# mc = MarkovChain(P, ['1', '2'])
# mc.draw()



# Gambling simulation
def gamblers_ruin():
    gambling_money = 50
    gambling_goal = 100
    gambling_simulations = []
    
    while gambling_money in range(1,gambling_goal):
        bet_size = 1
        w_or_l = random.randrange(-1,2,2)
        gambling_money+= bet_size * w_or_l
        gambling_simulations.append(gambling_money)
    return gambling_simulations



# Plotting Gambling Simulation
plt.plot(gamblers_ruin())
plt.yticks(np.arange(-20,120,10))
plt.axhline(y=0,color="red",linestyle ="-")
plt.axhline(y=100,color="black",linestyle ="-")
plt.xlabel("Numer of bets")
plt.ylabel("Winnings")
plt.title("Gambling Simulation")


# Probability of Ruin
def prob_of_ruin(gambling_goal, initial_gambling_money):
    return (gambling_goal - initial_gambling_money)/gambling_goal

prob_of_ruin(100,50)


sim_list = []
while len(sim_list) < 500:
    sim_list.append(gamblers_ruin()[-1])
np.mean(sim_list)




# Markov Chain Simulation
example = {
    "NYC":    [.25,0,.75,1],
    "Paris" : [.25,.25,0,0],
    "Cairo" : [.25,.25,.25,0],
    "Seoul" : [.25,.50,0,0]
}

markov_chain = pd.DataFrame(data=example,index = ["NYC","Paris","Cairo","Seoul"])
markov_chain

markov_chain_image  =  MarkovChain(markov_chain.to_numpy(), markov_chain.columns.tolist() )
# markov_chain_image.draw("./markov_chain.png")




# simulation for 25 times
travel_sim = []
travel_sim.append(markov_chain.iloc[0].index[0])
city = np.random.choice(markov_chain.iloc[0].index,p=markov_chain.iloc[0])
travel_sim.append(city)

while len(travel_sim) < 25:
    city = np.random.choice(markov_chain.iloc[markov_chain.index.get_loc(city)].index,p=markov_chain.iloc[markov_chain.index.get_loc(city)])
    travel_sim.append(city)

travel_sim



# n Step Transition Matrix

markov_chain.to_numpy();
def matrix_power(matrix,power):
    if power == 0:
        return np.identity(len(matrix)) 
    elif power == 1:
        return matrix
    else:
        return np.dot(matrix,matrix_power(matrix,power-1))


matrix_power(markov_chain,3)


# steady State Matrix 

for i in range (1,10,1):
    print(f'n step transition matrix at the nth power {i}\n',matrix_power(markov_chain,i),'\n')



# starting from a state where will it be in the next n steps

initial_dist = np.asarray([1,0,0,0])
mcp2 = matrix_power(markov_chain.to_numpy(),2)
np.dot(initial_dist,mcp2)