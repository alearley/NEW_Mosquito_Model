#!/usr/bin/python3
#Lattice version

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

class MosquitoSim:
    #Constructor
    def __init__(self, days, rate, var, initlocationList, model, horiz, vert):
        if len(initlocationList) != (horiz*vert):
            raise Exception('Error: the number of nodes and initial locations don\'t match')

        self.days = days
        self.rate = rate
        self.var = var
        self.locationList = initlocationList
        self.model = model
        self.horiz = horiz
        self.vert = vert

        self.xs = []
        self.ys = []

#Helper Methods
    def createLatt(self):
        latt = nx.Graph()
        for vPoint in range(self.vert):
            for hPoint in range(self.horiz - 1):
                firstCor= (vPoint * self.horiz) + hPoint
                latt.add_edges_from([(firstCor,firstCor+1)])
        for vPoint in range(self.vert-1):
            for hPoint in range(self.horiz):
                firstCor= (vPoint * self.horiz) + hPoint
                latt.add_edges_from([(firstCor,firstCor+self.horiz)])
        return(latt)
        #print (nx.info(latt))
        #nx.draw(latt, with_labels = True)
        
    def randomrate (self,num_mos,move_prob):
        return np.random.binomial(num_mos, move_prob)

    def distrmos(self,loc_idx,changemoslocs, latt):
        num_mos = self.locationList[loc_idx]
        if self.model == 'deterministic':
            mosmoving = num_mos*self.rate
        elif self.model == 'stochastic':
            mosmoving = np.random.binomial(self.var*num_mos, (1/self.var)*self.rate)
        else: raise Exception('Error: Please input deterministic or stochastic')
            

        self.locationList[loc_idx] -= mosmoving

        edlist = list(latt.adj[loc_idx])
        num_neighbors = len(edlist)
        if num_neighbors > 0:
            if self.model == 'deterministic':
                for ed in edlist:
                    changemoslocs[ed] += mosmoving/num_neighbors
            elif self.model == 'stochastic':
                counts = np.random.multinomial(mosmoving, [1.0/num_neighbors]*num_neighbors)
                for i in range(num_neighbors):
                    dest = edlist[i]
                    changemoslocs[dest] += counts[i]
            else: raise Exception('Error: Please input deterministic or stochastic')

    def simmos(self):
        latt= self.createLatt()
        loc_idxs = range(len(self.locationList))
        self.xs.append(0)
        for i in loc_idxs:
            self.ys.append([self.locationList[i]])

        for day in range(self.days):
            self.xs.append(day+1)
            changemoslocs = [0] * len(self.locationList)
            for i in loc_idxs:
                self.distrmos(i,changemoslocs,latt)
            for i in loc_idxs:
                self.locationList[i]+=changemoslocs[i]
                self.ys[i].append(self.locationList[i])


    def graph(self):
        print ('Days:', self.days)
        print ('Rate:', self.rate)
        if self.var != 1:
            if self.model == 'deterministic':
                print ('Note- Changing the variability doesn\'t affect deterministic models')
            elif self.model == 'stochastic':
                print('Variability factor:', self.var)
        for i in range(len(self.locationList)): plt.plot(np.array(self.xs),np.array(self.ys[i]),label = i)
        plt.xlabel('Days')
        plt.ylabel('Number of mosquitos')
        plt.title('Population of Mosquitos Over Time')
        plt.legend()
        plt.show()

    def simulateAndGraph(self):
        self.simmos()
        self.graph()

#g=nx.Graph()
#g.add_edges_from([(0,1),(1,2),(2,3),(3,0)])
#g.add_node(0)


#print (nx.info(g))
#nx.draw(g, with_labels = True)

'''
sims = [MosquitoSim(150,i/100,1,[10000,0,0,0],'stochastic') for i in range (20,21)] #last input should be 'stochastic' or 'deterministic'
for sim in sims: 
  sim.simmos()
  sim.graph()
'''

sim = MosquitoSim(100, 0.05, 0.05, [50, 50, 150, 50], 'deterministic', 2, 2)
#sim1 = MosquitoSim(100, 0.05, 0.05, [50,100,150,200], 'deterministic', g)

sim.simulateAndGraph()
#sim1.simulateAndGraph()