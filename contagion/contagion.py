#!/usr/bin/env python

"""
contagion.py
"""

__author__ = "Lucas McCabe"
__version__ = "JOSS"

import numpy as np
import networkx as nx
import random
from typing import List
import matplotlib.pyplot as plt
import seaborn as sns
import collections
import math
import scipy.special as scsp
from scipy.optimize import minimize
from numpy.linalg import matrix_power
import copy

class ContactNetwork():
    """For creating contact networks fron NetworkX graphs.
    """
    def __init__(
            self,
            G: nx.Graph,
            fraction_infected: float = 0,
            fraction_recovered: float = 0):
        """
        Constructor for the ContactNetwork class. Initializes a contact
        network with compartmental arrays.

        Parameters
        ----------
        G : `nx.Graph`
            a NetworkX graph
        fraction_infected : `float`
            portion of the population infected at initialization
            If not provided or provided with value 0, one node is selected
            to be infected.
        fraction_recovered : `float`
            portion of the population recovered at initialization

        Returns
        -------
        None
        """
        self.A = nx.adjacency_matrix(G).todense()
        self.n = len(self.A)
        self.G = G
        self.Mo = None
        self.Im = None
        self.mo_thresh = None
        self.im_starts_after = 0
        self.im_type = None
        self.efficacy = 1.
        if fraction_infected + fraction_recovered > 1.:
            raise ValueError('The size of the combined infected and recovered populations cannot be larger than the size of the graph.')
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
        self.init_Su_In_Re()
        return None

    def init_Su_In_Re(self):
        """Initializes susceptible, infected, and recovered arrays, ensuring
        there is no overlap/redundancy among them.

        Initializes
        -----------
        susceptible : `numpy.ndarray`
            array describing whether nodes are susceptible
        infected : `numpy.ndarray`
            array describing whether nodes are infected
        recovered : `numpy.ndarray`
            array describing whether nodes are recovered

        Returns
        -------
        None
        """
        infected_recovered = np.zeros(self.n)
        infected_recovered[:round(self.fraction_infected*self.n)] = 1
        infected_recovered[
            round(self.fraction_infected*self.n):
            round(
                self.fraction_infected*self.n
                + self.fraction_recovered*self.n)
            ] = 2
        np.random.shuffle(infected_recovered)
        infected = np.array(
            [1. if i == 1 else 0.
                for i in infected_recovered]).reshape(self.n, 1)
        recovered = np.array(
            [1. if i == 2 else 0.
                for i in infected_recovered]).reshape(self.n, 1)
        susceptible = np.ones(self.n).reshape(self.n, 1) - infected - recovered
        self.Su, self.In, self.Re = susceptible, infected, recovered
        self.og_Su, self.og_In, self.og_Re = copy.deepcopy(susceptible), copy.deepcopy(infected), copy.deepcopy(recovered)
        return None

    def reset_Su_In_Re(self):
        """Resets susceptible, infected, and recovered arrays to their original
        initializations.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.Su, self.In, self.Re = \
            copy.deepcopy(self.og_Su), \
            copy.deepcopy(self.og_In), \
            copy.deepcopy(self.og_Re)
        return None

    def generate_random_walk(self, walk_length: int = 1):
        """Generates an unbiased random walk of a specified length along the
        nodes/edges of the contact network. Elements of the walk are node
        indices.

        Parameters
        ----------
        walk_length : `int`
            number of nodes to include in the random walk

        Returns
        -------
        walk : `List`
            the node indices for the walk
        """
        walk = [random.choice([g for g in self.G])]
        while len(walk) < walk_length:
            walk.append(
                random.choice(
                    [n for n in self.G[walk[-1]]]))
        return walk

    def generate_random_walk_degree_sequence(self, walk_length: int = 1):
        """Generates an unbiased random walk of a specified length along the
        nodes/edges of the contact network and returns the degree of each node
        encountered during the walk.

        Parameters
        ----------
        walk_length : `int`
            number of nodes to include in the random walk

        Returns
        -------
        degrees : `List`
            the degree of each element of a random walk
        """
        walk = self.generate_random_walk(walk_length = walk_length)
        degrees = [len(self.G[i]) for i in walk]
        return degrees

    def immunize_network(
            self,
            Im,
            im_type = "vaccinate",
            im_starts_after = 0,
            efficacy = 1.,
            mo_thresh = 1):
        """Immunizes a network according to a provided Immunization array. The
        immunization array may be generated independently, or using the methods
        in the Immunization class. Immunization is either "vaccinate"
        (implemented by placing individuals in the Recovered compartment) or
        "monitor" (which tracks specified nodes, stopping a contagion simulation
        when mo_thresh monitored nodes have been ever infected).

        Parameters
        ----------
        Im : `numpy.ndarray`
            a (self.n, 1) array with 1 at indices to be immunized and 0 elsewhere
        im_type : `str`
            immunization type. Can be either "vaccinate" or "monitor"
        im_starts_after : `int`
            step index after which the immunization policy should be implemented
        efficacy : `float`
            efficacy of the immunization (as a float in [0, 1.])
            only operates with im_type == "vacciante".
        mo_thresh : `int`
            monitor threshold.

        Raises
        ------
        ValueError: when immunization array is the wrong dimensions
        ValueError: when invalid immunization type is provided.

        Returns
        -------
        None
        """
        if Im.shape == (self.n, 1):
            if im_type == "vaccinate":
                self.im_starts_after = im_starts_after
                self.Im = Im
                self.efficacy = efficacy

                if efficacy <= 0 or efficacy > 1:
                    raise ValueError("Invalid immunity type.")
            elif im_type == "monitor" and mo_thresh > 0:
                self.Mo = Im
                self.mo_thresh = mo_thresh
            else:
                raise ValueError("Invalid immunization type.")
            self.im_type = im_type
        else:
            raise ValueError("Incorrect dimensions for immunization array.")
        return None


class Contagion():
    """For running epidemiological simulations on contact networks.
    """
    def __init__(
            self,
            network: ContactNetwork,
            beta: float = 1.,
            gamma: float = 1.,
            save_history: bool = True,
            track_symptomatic: bool = False,
            psi: float = 1.,
            implement_testing: bool = False,
            testing_type: str = "random",
            test_rate: float = 0.,
            contagion_type: str = "sir"):
        """Constructor for the Contagion class.

        Parameters
        ----------
        network : `ContactNetwork`
            a specified contact network
        beta : `float`
            infection rate for susceptible nodes
        gamma : `float`
            recovery rate for an infected node
        save_history : `bool`
            describes whether to save susceptible, infected, and recovered
            histories for each time step
        track_symptomatic : `bool`
            describes whether to simulate the emergence of symptoms for
            modeling testing
        psi : `float`
            the rate at which infected nodes become symptomatic
        implement_testing : `bool`
            describes whether to simulate testing of the symptomatic
            population
        testing_type : `str`
            describes what testing strategy to use.
        test_rate : `float`
            portion(s) of nodes from population to test randomly. Can be
            float or tuple.
        contagion_type : `str`
            area for future development. currently must be "sir"

        Returns
        -------
        None
        """
        self.network = network
        self.save_history = save_history
        self.track_symptomatic = track_symptomatic
        self.implement_testing = implement_testing
        self.test_rate = test_rate
        if contagion_type.lower() not in ["sir"]:
            raise ValueError("Invalid contagion type provided.")
        else:
            self.contagion_type = contagion_type.lower()
        if 0. <= gamma <= 1.:
            # recovery rate for an infected node
            self.gamma = gamma
        else:
            raise ValueError('Gamma must be between 0 and 1.')
        if 0. <= beta <= 1.:
            # infection rate for susceptible nodes
            self.beta = beta
        else:
            raise ValueError('Beta must be between 0 and 1.')
        if 0. <= psi <= 1.:
            # the rate at which infected nodes become symptomatic
            self.psi = psi
        else:
            raise ValueError('Psi must be between 0 and 1.')

        self.new_transmissions = np.zeros((self.network.n, 1))
        self.new_recoveries = np.zeros((self.network.n, 1))

        if implement_testing:
            self.track_symptomatic = True  # to track symptomatic individuals
            self.network.EverTested = np.zeros((self.network.n, 1))
            # positive results from most recent test sample
            self.network.NewPositiveTests = np.zeros((self.network.n, 1))

            self.testing_type = testing_type
            if testing_type == "contact":
                self.contact_queue = []

        if track_symptomatic:
            self.network.Sy = np.zeros((self.network.n, 1))

        if save_history:
            self.init_histories()

        if self.network.im_type == "vaccinate" and 0 < self.network.efficacy < 1:
            self.Im_this_step = self.get_Im_random_filter()
            self.network.Re += self.Im_this_step
        return None

    def init_histories(self):
        """Initializes history tracking for susceptible, infected, recovered,
        and (if paramaterized) symptomatic and tested nodes.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.Su_hist = [np.sum(self.network.Su)]
        self.In_hist = [np.sum(self.network.In)]
        self.Re_hist = [np.sum(self.network.Re)]

        if self.track_symptomatic:
            self.Sy_hist = [np.sum(self.network.Sy)]

        if self.implement_testing:
            self.EverTested_hist = [np.sum(self.network.EverTested)]
            self.NewPositiveTests_hist = [
                np.sum(self.network.NewPositiveTests)]
        return None

    def get_Im_random_filter(self):
        """
        """
        if self.network.im_type == "vaccinate" and 0 < self.network.efficacy < 1:
            random_arr = np.random.rand(self.network.n, 1)
            Im_random_filter = np.multiply(self.network.Im, random_arr)
            Im_random_filter = np.where(
                (0 < Im_random_filter)
                & (Im_random_filter <= self.network.efficacy),
                1.,
                0.)
            return Im_random_filter
        else:
            raise ValueError("Immunization much be vaccination with partial efficacy.")

    def get_new_transmissions(self):
        """Calculates new infections in a time period.

        Parameters
        ----------
        None

        Returns
        -------
        new_transmissions : `np.ndarray`
            an array describing if nodes are new transmissions
        """
        # calculate neighbors of infected nodes
        new_transmissions = np.multiply(
                                np.matmul(
                                    self.network.A,
                                    self.network.In),
                                self.network.Su)
        # random transmission opportunities
        random_arr = np.random.rand(self.network.n, 1)
        new_transmissions = np.multiply(new_transmissions, random_arr)
        # filter with beta
        new_transmissions = np.where(
            (0 < new_transmissions)
            & (new_transmissions <= self.beta)
            & (self.network.Re == 0.), 1., 0.)
        return new_transmissions

    def get_new_recoveries(self):
        """Calculates new recoveries in a time period.

        Parameters
        ----------
        None

        Returns
        -------
        new_recoveries : `np.ndarray`
            an array describing if nodes are new recoveries
        """
        # random recovery opportunities
        random_arr = np.random.rand(self.network.n, 1)
        new_recoveries = np.multiply(self.network.In, random_arr)
        # filter with gamma
        new_recoveries = np.where(
            (0 < new_recoveries) & (new_recoveries <= self.gamma), 1., 0.)
        return new_recoveries

    def get_new_symptomatic(self):
        """Calculates new symptomatic infected nodes.

        Parameters
        ----------
        None

        Returns
        -------
        new_symptomatic : `np.ndarray`
            an array describing if nodes are newly-symptomatic nodes
        """
        asymptomatic_infected = self.network.In - self.network.Sy
        random_arr = np.random.rand(self.network.n, 1)
        new_symptomatic = np.multiply(asymptomatic_infected, random_arr)
        new_symptomatic = np.where(
            (0 < new_symptomatic) & (new_symptomatic <= self.psi), 1., 0.)
        return new_symptomatic

    def _get_new_tested_random(self):
        """Helper function for get_new_tested(). Supports random testing step.

        Parameters
        ----------
        None

        Returns
        -------
        new_tested : `np.ndarray`
            array of nodes with newly-administered tests

        Raises
        ------
        NotImplementedError
            Raised if test rate is not recognized.
        """
        if type(self.test_rate) is float:
            # if only one test rate is passed, interpret it as a naive
            # probability of any node being tested
            random_arr = np.random.rand(self.network.n, 1)
            new_tested = np.where(random_arr <= self.test_rate, 1., 0.)
        elif type(self.test_rate) is tuple:
            # if multiple test rates are passed, we specify different groups of
            # the population with different testing rates
            if len(self.test_rate) == 2:
                # interpret as (asymptomatic test rate, symptomatic test rate)
                # assumes recovered nodes do not get re-tested
                random_arr = np.random.rand(self.network.n, 1)
                # asymptomatics are individuals who are neither symptomatic
                # nor recovered
                asym = np.ones(
                    (self.network.n, 1))\
                    - self.network.Sy\
                    - self.network.Re
                new_asym_tested = np.where(
                    (random_arr <= self.test_rate[0]) & (asym == 1.), 1., 0.)
                new_sym_tested = np.where(
                    (random_arr <= self.test_rate[1])
                    & (self.network.Sy == 1.), 1., 0.)
                new_tested = new_asym_tested + new_sym_tested
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
        return new_tested

    def _get_new_tested_contact(self):
        """Helper function for get_new_tested(). Supports contact tracing testing
        step.

        Parameters
        ----------
        None

        Returns
        -------
        new_tested : `np.ndarray`
            array of nodes with newly-administered tests

        Raises
        ------
        NotImplementedError
            Raised if test rate is not recognized.
        """
        if np.sum(self.network.NewPositiveTests) == 0 or \
                len(self.contact_queue) == 0:
            new_tested = self._get_new_tested_random()
        elif type(self.test_rate) is float:
            number_to_test = int(self.test_rate*self.network.n)
            if number_to_test <= len(self.contact_queue):
                new_tested_queue = self.contact_queue[:number_to_test]
                self.contact_queue = self.contact_queue[number_to_test:]
            else:
                new_tested_queue = self.contact_queue
                new_tested_queue += random.sample(
                    [i for i in range(self.network.n)
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
        """Selects new nodes for testing. Re-testing is permitted. Default
        testing strategy is uniform random testing, although contact tracing
        ("contact") is also available.

        Parameters
        ----------
        None

        Returns
        -------
        new_tested : `np.ndarray`
            array of nodes with newly-administered tests
        new_ever_tested : `np.ndarray`
            array of nodes with newly-administered tests who have not been
            tested before

        Raises
        ------
        NotImplementedError
            Raised if test rate is not recognized.
        """
        if self.testing_type == "random":
            new_tested = self._get_new_tested_random()
        elif self.testing_type == "contact":
            new_tested = self._get_new_tested_contact()
        else:
            raise NotImplementedError

        new_ever_tested = np.where(
            (new_tested == 1.) & (self.network.EverTested == 0.), 1., 0.)
        return new_tested, new_ever_tested

    def get_new_testedpositive(self):
        """New positive tests are newly-administered tests of infected patients.

        Parameters
        ----------
        None

        Returns
        -------
        new_testedpositive : `np.ndarray`
            array describing if nodes are new positive tests
        """
        new_testedpositive = np.where(
            (self.new_tested == 1.) & (self.network.In == 1.), 1., 0.)
        return new_testedpositive

    def update_Su(self):
        """Updates susceptible record with new transmissions.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.network.Su -= self.new_transmissions
        if self.save_history:
            self.Su_hist.append(np.sum(self.network.Su))
        return None

    def update_In(self):
        """Updates infected record with new transmissions and new recoveries.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.network.In += self.new_transmissions - self.new_recoveries
        if self.save_history:
            self.In_hist.append(np.sum(self.network.In))
        return None

    def update_Re(self):
        """Updates recovered record with new recoveries.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Raised if contagion type is invalid.
        """
        if self.contagion_type == "sir":
            self.network.Re += self.new_recoveries
            self.network.Re = np.where(self.network.Re > 0, 1., 0.)

            if self.save_history:
                self.Re_hist.append(np.sum(self.network.Re))
        else:
            raise ValueError("Invalid contagion type.")
        return None

    def update_Sy(self):
        """Updates symptomatic record with new symptomatic infected nodes.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.network.Sy += self.new_symptomatic - self.new_recoveries
        if self.save_history:
            self.Sy_hist.append(np.sum(self.network.Sy))
        return None

    def update_EverTested(self):
        """Updates record of nodes ever tested with recent tests.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.network.EverTested += self.new_ever_tested
        if self.save_history:
            self.EverTested_hist.append(np.sum(self.network.EverTested))
        return None

    def _get_new_contact_queue(self):
        """Helper function for self.simulate_step(). Selects new nodes to update
        the contact queue.

        Parameters
        ----------
        None

        Returns
        -------
        li : `List`
            list of new nodes for the contact queue
        """
        contact_arr = np.dot(self.network.A, self.network.NewPositiveTests)
        return [i for i in range(self.network.n) if contact_arr[i] > 0]

    def simulate_step(self):
        """Iterates a single simulation time step, updating susceptible,
        infected, and recovered records with new transmissions and recoveries.
        Handles delayed immunization and "switching out" for partial immunity.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self.network.im_type == "vaccinate" \
                and self.network.efficacy == 1 \
                and len(self.In_hist) - 1 == self.network.im_starts_after:
            self.network.Re += self.network.Im
            self.network.Re = np.where(self.network.Re > 0, 1., 0.)

        if self.network.im_type == "vaccinate" \
                and 0 < self.network.efficacy < 1 \
                and len(self.In_hist) - 1 >= self.network.im_starts_after:
            self.network.Re -= self.Im_this_step
            self.network.Re = np.where(self.network.Re >  0, 1., 0.)
            self.Im_this_step = self.get_Im_random_filter()
            self.network.Re += self.Im_this_step
            self.network.Re = np.where(self.network.Re > 0, 1., 0.)

        # update new records
        self.new_transmissions = self.get_new_transmissions()
        self.new_recoveries = self.get_new_recoveries()

        if self.track_symptomatic:
            self.new_symptomatic = self.get_new_symptomatic()

        if self.implement_testing:
            self.new_tested, self.new_ever_tested = self.get_new_tested()
            self.network.NewPositiveTests = self.get_new_testedpositive()

            if self.testing_type == "contact":
                self.contact_queue += self._get_new_contact_queue()
        # update historical records
        self.update_Su()
        self.update_In()
        self.update_Re()
        if self.track_symptomatic:
            self.update_Sy()
        if self.implement_testing:
            self.update_EverTested()
            self.NewPositiveTests_hist.append(
                np.sum(self.network.NewPositiveTests))
        return None

    def run_simulation(self, steps: float = np.inf):
        """Runs a contagion simulation for the specified number of steps. If
        step count is not provided, runs until infectivity subsides.

        Paramaters
        ----------
        steps : `float`
            number of simulation steps to run.

        Returns
        -------
        None
        """
        # turn histories on
        if not self.save_history:
            self.init_histories()
            self.save_history = True
        # run simulation
        i = 0
        while i < steps:
            if len(self.In_hist) > 5 and \
                    (self.In_hist[-1] == 0 or self.In_hist[-1] == self.network.n):
                break
            self.simulate_step()
            i += 1
        return None

    def run_simulation_get_max_infected(self, steps: float = np.inf):
        """Runs a contagion simulation and returns the maximum number of
        infected individuals at any step.

        Parameters
        ----------
        steps : `float`
            number of simulation steps to run.

        Returns
        -------
        num : `int`
            maximum number of infected individuals at any simulation step.
        """
        self.run_simulation(steps)
        return np.max(self.In_hist)

    def run_simulation_monitor_notification(self):
        """Runs an epidemic simulation up to the point that a threshold number
        of monitored individual are (ever) infected.

        Parameters
        ----------
        None

        Returns
        -------
        num : `int`
            time-step when threshold number of monitored individual were (ever)
            infected
        """
        # turn histories on
        if not self.save_history:
            self.init_histories()
            self.save_history = True

        if self.network.Mo is None or self.network.mo_thresh is None:
            raise ValueError("Monitoring not initialized.")

        ever_monitored_infected_arr = np.zeros((self.network.n, 1))
        # run simulation
        while np.count_nonzero(
                ever_monitored_infected_arr) < self.network.mo_thresh:
            if len(self.In_hist) > 5 and self.In_hist[-1] == 0:
                break
            self.simulate_step()
            curr_monitored_infected_arr = self.network.Mo*self.network.In
            ever_monitored_infected_arr = np.where(
                (ever_monitored_infected_arr>0) | (curr_monitored_infected_arr>0),
                1.,
                0.)
        return len(self.In_hist)

    def run_simulation_get_max_infected_index(self, steps = np.inf):
        """
        Runs an epidemic simulation and returns the step at which the greatest
        number of infected individuals was reached.

        Parameters
        ----------
        steps : `int`
            number of simulation steps to run.

        Returns
        -------
        Historical index of maximum number of infected individuals.
        """
        max_infected = self.run_simulation_get_max_infected(steps)

        return self.In_hist.index(max_infected)

    def plot_simulation(self, steps: float = np.inf):
        """Runs an epidemic simulation and produces a corresponding simulation
        history figure.

        Parameters
        ----------
        steps : `float`
            number of simulation steps to run.
        """
        # run simulation
        self.run_simulation(steps)

        # generate figure
        sns.set_style("white")
        plt.plot(self.Su_hist, label="Susceptible")
        plt.plot(self.Re_hist, label="Recovered")

        if self.track_symptomatic:
            plt.plot(self.In_hist, label="Infected Total")
            plt.plot(self.Sy_hist, label="Infected Symptomatic")
            infected_asymptomatic = [
                self.In_hist[i] - self.Sy_hist[i] for i in range(steps)]
            plt.plot(infected_asymptomatic, label="Infected Asymptomatic")
        else:
            plt.plot(self.In_hist, label="Infected")

        if self.implement_testing:
            plt.plot(self.EverTested_hist, label="Nodes Ever Tested")
            plt.plot(self.NewPositiveTests_hist, label="New Positive Tests")

        plt.title("Simulation Compartmental Histories")
        plt.xlabel("Simulation Time")
        plt.ylabel("Count of Nodes")
        plt.ylim(0., self.network.n)
        plt.legend()
        sns.despine()
        plt.show()
        return None

class Immunization():
    """Some baseline algorithms for generating immunization arrays."""

    def __init__(self, network):
        """Constructor for the Immunization class.

        Parameters
        ----------
        network : `ContactNetwork`
            a specified contact network

        Returns
        -------
        None
        """
        self.network = network
        return None

    def generate_random_immunization_array(self, Q = 1):
        """
        Generates an immunization array with Q nodes randomly immunized.

        Parameters
        ----------
        Q : `int`
            Number of individuals to immunize; default to 1

        Returns
        -------
        Im : `numpy.ndarray`
            an (n, 1) array with 1 at indices to be immunized and 0 elsewhere
        """
        Im = np.zeros(self.network.n)
        Im[:Q] = 1
        np.random.shuffle(Im)
        return Im.reshape(self.network.n, 1)

    def generate_highest_degrees_immunization_array(self, Q = 1):
        """
        Generates an immunization array with the Q highest-degree nodes
        immunized.

        Parameters
        ----------
        Q : `int`
            Number of individuals to immunize; default to 1

        Returns
        -------
        Im : `numpy.ndarray`
            an (n, 1) array with 1 at indices to be immunized and 0 elsewhere
        """
        Im = np.zeros(self.network.n)
        for i in [node[0] for node in \
                sorted(self.network.G.degree, key=lambda x: x[1], reverse=True)][:Q]:
            Im[i] = 1
        return Im.reshape(self.network.n, 1)

    def generate_lowest_degrees_immunization_array(self, Q = 1):
        """
        Generates an immunization array with the Q lowest-degree nodes
        immunized.

        Parameters
        ----------
        Q : `int`
            Number of individuals to immunize; default to 1

        Returns
        -------
        Im : `numpy.ndarray`
            an (n, 1) array with 1 at indices to be immunized and 0 elsewhere
        """
        Im = np.zeros(self.network.n)
        for i in [node[0] for node in \
                sorted(self.network.G.degree, key=lambda x: x[1], reverse=False)][:Q]:
            Im[i] = 1
        return Im.reshape(self.network.n, 1)

    def generate_centrality_immunization_array(
            self,
            Q = 1,
            centrality_type = "betweenness",
            order = "highest"):
        """
        Generates an immunization array with the Q lowest or highest centrality
        nodes immunized. Three measures of centrality are implemented:
        betweenness, eigenvector, and closeness.

        Parameters
        ----------
        Q : `int`
            Number of individuals to immunize; default to 1
        centrality_type : `str`
            Flavor of centrality to use. Defaults to betweenness
        order : `str`
            Either "highest" or "lowest"

        Returns
        -------
        Im : `numpy.ndarray`
            an (n, 1) array with 1 at indices to be immunized and 0 elsewhere

        Raises
        ------
        NotImplementedError : for invalid centrality type or how not in
            ["highest", "lowest"]
        """
        Im = np.zeros(self.network.n)

        if centrality_type == "betweenness":
            centralities = nx.betweenness_centrality(self.network.G)
        elif centrality_type == "eigenvector":
            centralities = nx.eigenvector_centrality(self.network.G)
        elif centrality_type == "closeness":
            centralities = nx.closeness_centrality(self.network.G)
        else:
            raise NotImplementedError

        if order == "lowest":
            for i in sorted(
                    centralities, key=lambda x: centralities[x], reverse=False)[:Q]:
                Im[i] = 1
        elif order == "highest":
            for i in sorted(
                    centralities, key=lambda x: centralities[x], reverse=True)[:Q]:
                Im[i] = 1
        else:
            raise NotImplementedError
        return Im.reshape(self.network.n, 1)
