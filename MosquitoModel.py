import random
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import math

class MosquitoSim:
  #Constructor
  def __init__(self, days, rate, pervar, initlocationList, randomness, netgraph):
    if len(initlocationList) != len(netgraph):
      raise Exception('Error: the number of notes and initial locations don\'t match')
      
    self.days = days
    self.rate = rate
    self.pervar = pervar
    self.locationList = initlocationList
    self.randomness = randomness
    self.netgraph = netgraph
    
    self.xs = [0]
    self.ys = [0]
    self.shouldround = False
	
#Helper Methods
  def rounddecimal (self,number):
    if int(number) == number-0.5: return int(number) + 1
    else: return round(number)

  def randomrate (self,value):
    numMosquitos = np.random.normal(value, (math.sqrt(value*0.25)*self.pervar))
    if numMosquitos < 0:
      return 0
    elif numMosquitos > 2*value:
      return 2*value
    else:
      return numMosquitos
    '''total = 0
    for b in range (0, 2*int(value)):
      c = random.randint(0,1)
      total += c
    return (total)'''

  def distrmos(self,loc0,inputlist):
    if self.randomness == "ideal":
      mosmoving = self.locationList[loc0]*self.rate*self.pervar
    else:
      mosmoving = self.randomrate(self.locationList[loc0]*self.rate)
    self.locationList[loc0] -= mosmoving
    edlist = list(self.netgraph.adj[loc0])
    if len(edlist) > 0:
        if self.randomness == "ideal":
          for ed in edlist:
            inputlist[ed] += mosmoving/(len(edlist))
        else:
          for mos in range (0,mosmoving):
            rand = random.randint(0,len(edlist)-1)
            d = edlist[rand]
            inputlist[d] +=1

  def simmos(self):

    for loc1 in range (0,len(self.locationList)): self.ys.append ([self.locationList[loc1]])

    for day in range (1,self.days+1):
      self.xs.append (day)
      while True:
        changemoslocs= [0] * len(self.locationList)
        totalmos = 0
        for loc2 in range (0,len(self.locationList)): totalmos += self.locationList[loc2]
        for loc3 in range (0,len(self.locationList)): self.distrmos(loc3,changemoslocs)
        for loc4 in range (0,len(self.locationList)-1): self.locationList[loc4]+=changemoslocs[loc4]
        self.locationList[len(self.locationList)-1] = totalmos
        for loc5 in range (0,len(self.locationList)-1): self.locationList[len(self.locationList)-1] -= self.locationList[loc5]
        for loc6 in range (0,len(self.locationList)): 
          if self.locationList[loc6] < 0: continue
        for loc7 in range (1,len(self.locationList)+1): 
          self.ys[loc7].append (self.locationList[(loc7-1)])
        break

  def graph(self):
    print ("Days:", self.days)
    print ("Rate:", self.rate)
    for loc8 in range (1,len(self.locationList)+1): plt.plot(np.array(self.xs),np.array(self.ys[loc8]),label = (loc8-1))
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
h.add_edges_from([(0,1),(1,0)])
#print (nx.info(g))
#nx.draw(g, with_labels = True)

'''
sims = [MosquitoSim(150,i/100,1,[10000,0,0,0],'random') for i in range (20,21)] #last input should be 'random' or 'ideal'
#for sim in sims: #I still don't understand exactly why we're doing this. It seems to be running these portions over again.
  #sim.simmos()
  #sim.graph()
'''
  
 
sim = MosquitoSim(150,4/100,1,[1000,0,5,0],'random', g)
sim1 = MosquitoSim(150,4/100,1,[500,0],'ideal', h)
#sim1.shouldround = True

sim.simulateAndGraph()
sim1.simulateAndGraph()
