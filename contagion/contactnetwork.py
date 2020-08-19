#!/usr/bin/env python

"""
contactnetwork.py: Consists of a single class for creating a contact network for
a contagion model.
"""

__author__ = "Lucas McCabe"
__status__ = "Development"

import numpy as np
import networkx as nx
import random

class ContactNetwork():
	def __init__(self,
					G: nx.Graph,
					fraction_infected: float = 0,
					fraction_recovered: float = 0):
		"""
		Constructor for the ContactNetwork class.

		Parameters:
			G: a networkx graph
			fraction_infected: portion of the population infected at
				initialization
			fraction_recovered: portion of the population recovered at
				initialization
		Initializes:
			A: adjacency matrix for the graph G
			n: number of individuals in population
			fraction_infected: as above, portion of the population infected at
				initialization. If fraction_infected == 0, one node is infected
				at initialization.
			Su: vector of susceptible nodes
			In: vector of infected nodes
			Re: vector of recovered nodes
		"""
		self.A = nx.adjacency_matrix(G).todense()
		self.n = len(self.A)
		self.G = G

		if fraction_infected + fraction_recovered > 1.:
			raise ValueError('Fraction infected/recovered must be at most 1.')

		if fraction_infected == 0.:
			self.fraction_infected = 1./self.n
		elif 0. < fraction_infected <= 1.:
			self.fraction_infected = fraction_infected
		else:
			raise ValueError('Fraction infected must be between 0 and 1.')

		if 0. <= fraction_recovered <= 1.:
			self.fraction_recovered = fraction_recovered
		else:
			raise ValueError('Fraction recovered must be between 0 and 1.')

		self.Su, self.In, self.Re = self.init_Su_In_Re()


	def init_Su_In_Re(self):
		"""
		Initializes susceptible, infected, and recovered vectors, ensuring
		there is no overlap/redundancy among them.
		"""
		infected_recovered = np.zeros(self.n)
		infected_recovered[:round(self.fraction_infected*self.n)] = 1
		infected_recovered[round(self.fraction_infected*self.n):
							round(self.fraction_infected*self.n
									+ self.fraction_recovered*self.n)] = 2
		np.random.shuffle(infected_recovered)
		infected = np.array([1. if i==1 else 0. for i in infected_recovered]
							).reshape(self.n,1)
		recovered = np.array([1. if i==2 else 0. for i in infected_recovered]
							).reshape(self.n,1)
		susceptible = np.ones(self.n).reshape(self.n,1) - infected - recovered
		return susceptible, infected, recovered
