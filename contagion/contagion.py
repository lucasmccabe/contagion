#!/usr/bin/env python

"""
contagion.py: Consists of a single class for implementing a contagion model on a
contact network.
"""

__author__ = "Lucas McCabe"
__status__ = "Development"

from typing import Tuple, List
import numpy as np
import networkx as nx
import random
import matplotlib.pyplot as plt
import seaborn as sns
from contactnetwork import ContactNetwork

class Contagion():
    def __init__(self,
                    network: ContactNetwork,
                    contagion_type: str = "sir",
                    beta: float = 1.,
                    gamma: float = 1.,
                    save_history: bool = True,
                    track_symptomatic: bool = False,
                    psi: float = 1.,
                    implement_testing: bool = False,
                    testing_type: str = "random",
                    test_rate: float = 0.):
        """
        Constructor for the Contagion class.

        Parameters:
            network: a specified contact network
            contagion_type: either "sir" or "sis"
            beta: infection rate for susceptible nodes
            gamma: recovery rate for an infected node
            save_history: describes whether to save susceptible, infected, and
                recovered histories for each time step
            track_symptomatic: describes whether to simulate the emergence of
                symptoms for modeling testing
            psi: the rate at which infected nodes become symptomatic
            implement_testing: describes whether to simulate testing of the
                symptomatic population
            testing_type: describes what testing strategy to use. Currently:
                random: uniform random sample of available populatio
            test_rate: portion(s) of nodes from population to test randomly.
                Can be float or tuple.
        """
        self.network = network
        self.save_history = save_history
        self.track_symptomatic = track_symptomatic
        self.implement_testing = implement_testing
        self.test_rate = test_rate
        if contagion_type.lower() not in ["sir", "sis"]:
            raise ValueError("Invalid contagion type provided.")
        else:
            self.contagion_type = contagion_type.lower()

        if 0. <= gamma <= 1.:
            #recovery rate for an infected node
            self.gamma = gamma
        else:
            raise ValueError('Gamma must be between 0 and 1.')

        if 0. <= beta <= 1.:
            #infection rate for susceptible nodes
            self.beta = beta
        else:
            raise ValueError('Beta must be between 0 and 1.')

        if 0. <= psi <= 1.:
            #the rate at which infected nodes become symptomatic
            self.psi = psi
        else:
            raise ValueError('Psi must be between 0 and 1.')

        self.new_transmissions = np.zeros((self.network.n,1))
        self.new_recoveries = np.zeros((self.network.n,1))

        if implement_testing:
            self.track_symptomatic = True #to track symptomatic individuals
            self.network.EverTested = np.zeros((self.network.n,1)) #tested nodes
            #positive results from most recent test sample
            self.network.NewPositiveTests = np.zeros((self.network.n,1))

            self.testing_type = testing_type
            if testing_type == "contact":
                self.contact_queue = []

        if track_symptomatic:
            self.network.Sy = np.zeros((self.network.n, 1)) #symptomatic nodes

        if save_history:
            self.init_histories()


    def init_histories(self):
        """
        Initializes history tracking for susceptible, infected, recovered, and
        (if paramaterized) symptomatic and tested nodes.
        """
        self.Su_hist = [np.sum(self.network.Su)]
        self.In_hist = [np.sum(self.network.In)]
        self.Re_hist = [np.sum(self.network.Re)]

        if self.track_symptomatic:
            self.Sy_hist = [np.sum(self.network.Sy)]

        if self.implement_testing:
            self.EverTested_hist = [np.sum(self.network.EverTested)]
            self.NewPositiveTests_hist = [np.sum(self.network.NewPositiveTests)]

        if self.track_class_ratios:
            self.class_ratio_hist = []
        return None

    def get_new_transmissions(self) -> np.ndarray:
        """
        Calculates new infections in a time period.
        """
        #calculate neighbors of infected nodes
        new_transmissions = np.multiply(
                                np.matmul(
                                    self.network.A,
                                    self.network.In),
                                self.network.Su)
        #random transmission opportunities
        random_arr = np.random.rand(self.network.n,1)
        new_transmissions = np.multiply(new_transmissions, random_arr)
        #filter with beta
        new_transmissions = np.where((0<new_transmissions)
                                    & (new_transmissions<=self.beta)
                                    & (self.network.Re==0.), 1., 0.)
        return new_transmissions

    def get_new_recoveries(self) -> np.ndarray:
        """
        Calculates new recoveries in a time period.
        """
        #random recovery opportunities
        random_arr = np.random.rand(self.network.n,1)
        new_recoveries = np.multiply(self.network.In, random_arr)
        #filter with gamma
        new_recoveries = np.where((0<new_recoveries)
                                & (new_recoveries<=self.gamma), 1., 0.)
        return new_recoveries

    def get_new_symptomatic(self) -> np.ndarray:
        """
        Calculates new symptomatic infected nodes.
        """
        asymptomatic_infected = self.network.In - self.network.Sy
        random_arr = np.random.rand(self.network.n,1)
        new_symptomatic = np.multiply(asymptomatic_infected, random_arr)
        new_symptomatic = np.where((0<new_symptomatic)
                                & (new_symptomatic<=self.psi), 1., 0.)
        return new_symptomatic

    def _get_new_tested_random(self):
        """
        Helper function for get_new_tested(). Supports random testing step.

        Returns:
            new_tested: np.ndarray of nodes with newly-administered tests
        Raises:
            NotImplementedError for unrecognized test rate
        """
        if type(self.test_rate) is float:
            #if only one test rate is passed, interpret it as a naive
            #probability of any node being tested
            random_arr = np.random.rand(self.network.n,1)
            new_tested = np.where(random_arr<=self.test_rate, 1., 0.)
        elif type(self.test_rate) is tuple:
            #if multiple test rates are passed, we specify different groups of
            #the population with different testing rates
            if len(self.test_rate) == 2:
                #interpret as (asymptomatic test rate, symptomatic test rate)
                #assumes recovered nodes do not get re-tested
                random_arr = np.random.rand(self.network.n,1)
                #asymptomatics are individuals who are neither symptomatic
                #nor recovered
                asym = np.ones((self.network.n,1))\
                                - self.network.Sy\
                                - self.network.Re
                new_asym_tested = np.where((random_arr <= self.test_rate[0])
                                    & (asym == 1.), 1., 0.)
                new_sym_tested = np.where((random_arr<=self.test_rate[1])
                                    & (self.network.Sy==1.), 1., 0.)
                new_tested = new_asym_tested + new_sym_tested
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
        return new_tested

    def _get_new_tested_contact(self):
        """
        Helper function for get_new_tested(). Supports contact tracing testing
        step.

        Returns:
            new_tested: np.ndarray of nodes with newly-administered tests
        Raises:
            NotImplementedError for unrecognized test rate
        """
        if np.sum(self.network.NewPositiveTests) == 0 or \
                                                    len(self.contact_queue)==0:
            new_tested = self._get_new_tested_random()
        elif type(self.test_rate) is float:
            number_to_test = int(self.test_rate*self.network.n)
            if number_to_test <= len(self.contact_queue):
                new_tested_queue = self.contact_queue[:number_to_test]
                self.contact_queue = self.contact_queue[number_to_test:]
            else:
                new_tested_queue = self.contact_queue
                new_tested_queue += random.sample(
                                        [i for i in range(self.network.n) \
                                            if i not in new_tested_queue],
                                        number_to_test-len(self.contact_queue))
                self.contact_queue = []
            new_tested = np.zeros((self.network.n, 1))
            for i in new_tested_queue:
                new_tested[i] = 1
        else:
            raise NotImplementedError
        return new_tested

    def get_new_tested(self):
        """
        Selects new nodes for testing. Re-testing is permitted. Default testing
        strategy is uniform random testing, although contact tracing ("contact")
        is also permitted.

        Returns:
            new_tested: np.ndarray of nodes with newly-administered tests
            new_ever_tested: np.ndarray of nodes with newly-administered tests
                who have not been tested before
        """
        if self.testing_type == "random":
            new_tested = self._get_new_tested_random()
        elif self.testing_type == "contact":
            new_tested = self._get_new_tested_contact()
        else:
            raise NotImplementedError

        new_ever_tested = np.where((new_tested == 1.)
                            & (self.network.EverTested == 0.), 1., 0.)
        return new_tested, new_ever_tested

    def get_new_testedpositive(self) -> np.ndarray:
        """
        New positive tests are newly-administered tests of infected patients.
        """
        new_testedpositive = np.where((self.new_tested == 1.)
                                    &(self.network.In == 1.), 1., 0.)
        return new_testedpositive

    def update_Su(self):
        """
        Updates susceptible record with new transmissions.
        """
        self.network.Su -= self.new_transmissions
        if self.save_history:
            self.Su_hist.append(np.sum(self.network.Su))
        return None

    def update_In(self):
        """
        Updates infected record with new transmissions and new recoveries.
        """
        self.network.In += self.new_transmissions - self.new_recoveries
        if self.save_history:
            self.In_hist.append(np.sum(self.network.In))
        return None

    def update_Re(self):
        """
        Updates recovered record with new recoveries.
        """
        if self.contagion_type == "sir":
            self.network.Re += self.new_recoveries
            if self.save_history:
                self.Re_hist.append(np.sum(self.network.Re))
        elif self.contagion_type == "sis":
            self.network.Su += self.new_recoveries
            if self.save_history:
                self.Su_hist[-1] = np.sum(self.network.Su)
        else:
            raise ValueError("Invalid contagion type.")
        return None

    def update_Sy(self):
        """
        Updates symptomatic record with new symptomatic infected nodes.
        """
        self.network.Sy += self.new_symptomatic - self.new_recoveries
        if self.save_history:
            self.Sy_hist.append(np.sum(self.network.Sy))
        return None

    def update_EverTested(self):
        """
        """
        self.network.EverTested += self.new_ever_tested
        if self.save_history:
            self.EverTested_hist.append(np.sum(self.network.EverTested))
        return None

    def _get_new_contact_queue(self):
        """
        """
        contact_arr = np.dot(self.network.A, self.network.NewPositiveTests)
        return [i for i in range(self.network.n) if contact_arr[i]>0]

    def simulate_step(self):
        """
        Iterates a single simulation time step, updating susceptible, infected,
        and recovered records with new transmissions and recoveries.
        """
        #update new records
        self.new_transmissions = self.get_new_transmissions()
        self.new_recoveries = self.get_new_recoveries()

        if self.track_symptomatic:
            self.new_symptomatic = self.get_new_symptomatic()

        if self.implement_testing:
            self.new_tested, self.new_ever_tested = self.get_new_tested()
            self.network.NewPositiveTests = self.get_new_testedpositive()

            if self.testing_type == "contact":
                self.contact_queue += self._get_new_contact_queue()

        #update historical records
        self.update_Su()
        self.update_In()
        self.update_Re()
        if self.track_symptomatic:
            self.update_Sy()
        if self.implement_testing:
            self.update_EverTested()
            self.NewPositiveTests_hist.append(np.sum(
                                                self.network.NewPositiveTests))
        return None

    def plot_simulation(self, steps: int = 100):
        """
        Runs an epidemic simulation and produces a corresponding simulation
        history figure.

        Parameters:
            steps: number of simulation steps to run.
        """
        #turn histories on
        if not self.save_history:
            self.init_histories()
            self.save_history = True

        #run simulation
        for i in range(steps):
            self.simulate_step()

        #generate figure
        sns.set_style("darkgrid")
        plt.plot(self.Su_hist,
                label = "Susceptible")
        plt.plot(self.Re_hist,
                label = "Recovered")

        if self.track_symptomatic:
            plt.plot(self.In_hist,
                    label = "Infected Total")
            plt.plot(self.Sy_hist,
                    label = "Infected Symptomatic")
            infected_asymptomatic = [self.In_hist[i]-self.Sy_hist[i]
                                                        for i in range(steps)]
            plt.plot(infected_asymptomatic,
                    label = "Infected Asymptomatic")
        else:
            plt.plot(self.In_hist,
                    label = "Infected")

        if self.implement_testing:
            plt.plot(self.EverTested_hist,
                    label = "Nodes Ever Tested")
            plt.plot(self.NewPositiveTests_hist,
                    label = "New Positive Tests")

        plt.title("Simulation Compartmental Histories")
        plt.xlabel("Simulation Time")
        plt.ylabel("Count of Nodes")
        plt.ylim(0., self.network.n)
        plt.legend()
        plt.show()
        return None
