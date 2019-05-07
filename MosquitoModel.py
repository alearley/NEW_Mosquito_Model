#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

class MosquitoSim:
    #Constructor
    def __init__(self, days, rate, var, initlocationList, randomness, netgraph):
        if len(initlocationList) != len(netgraph):
            raise Exception('Error: the number of notes and initial locations don\'t match')

        self.days = days
        self.rate = rate
        self.var = var
        self.locationList = initlocationList
        self.randomness = randomness
        self.netgraph = netgraph

        self.xs = []
        self.ys = []

#Helper Methods
    def randomrate (self,num_mos,move_prob):
        return np.random.binomial(num_mos, move_prob)

    def distrmos(self,loc_idx,changemoslocs):
        num_mos = self.locationList[loc_idx]
        if self.randomness == "deterministic":
            mosmoving = num_mos*self.rate*self.var
        elif self.randomness == "stochastic":
            mosmoving = np.random.binomial(num_mos, self.rate)
        else: raise Exception('Error: Please input deterministic or stochastic')
            

        self.locationList[loc_idx] -= mosmoving

        edlist = list(self.netgraph.adj[loc_idx])
        num_neighbors = len(edlist)
        if num_neighbors > 0:
            if self.randomness == "deterministic":
                for ed in edlist:
                    changemoslocs[ed] += mosmoving/num_neighbors
            elif self.randomness == "stochastic":
                counts = np.random.multinomial(mosmoving, [1.0/num_neighbors]*num_neighbors)
                for i in range(num_neighbors):
                    dest = edlist[i]
                    changemoslocs[dest] += counts[i]
            else: raise Exception('Error: Please input deterministic or stochastic')

    def simmos(self):
        loc_idxs = range(len(self.locationList))
        self.xs.append(0)
        for i in loc_idxs:
            self.ys.append([self.locationList[i]])

        for day in range(self.days):
            self.xs.append(day+1)
            changemoslocs = [0] * len(self.locationList)
            for i in loc_idxs:
                self.distrmos(i,changemoslocs)
            for i in loc_idxs:
                self.locationList[i]+=changemoslocs[i]
                self.ys[i].append(self.locationList[i])


    def graph(self):
        print ("Days:", self.days)
        print ("Rate:", self.rate)
        for i in range(len(self.locationList)): plt.plot(np.array(self.xs),np.array(self.ys[i]),label = i)
        plt.xlabel('Days')
        plt.ylabel('Number of mosquitos')
        plt.title('Population of Mosquitos Over Time')
        plt.legend()
        plt.show()

    def simulateAndGraph(self):
        self.simmos()
        self.graph()

g=nx.Graph()
g.add_edges_from([(0,1),(1,2),(2,3),(3,0)])
#g.add_node(0)

h = nx.Graph()
h.add_edges_from([(0,1),(1,2),(2,0)])
#print (nx.info(g))
#nx.draw(g, with_labels = True)

'''
sims = [MosquitoSim(150,i/100,1,[10000,0,0,0],'stochastic') for i in range (20,21)] #last input should be 'stochastic' or 'deterministic'
for sim in sims: 
  sim.simmos()
  sim.graph()
'''

sim = MosquitoSim(10, 0.05, 1, [30,23,45,23], 'stochastic', g)
sim1 = MosquitoSim(25, 0.04, 1, [234,574,326], 'deterministic', h)

sim.simulateAndGraph()
sim1.simulateAndGraph()