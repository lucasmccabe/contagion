import sys
import copy
import unittest
import numpy as np
import networkx as nx
sys.path.append("..")
from contagion import contagion


class TestContagion(unittest.TestCase):

    def test_init_In(self):
        """
        Tests initialization of Infected compartment.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.5,
            fraction_recovered = 0.35)
        self.assertEqual(np.sum(network.In), 50)

    def test_init_Su(self):
        """
        Tests initialization of Susceptible compartment.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.5,
            fraction_recovered = 0.35)
        self.assertEqual(np.sum(network.Su), 15)

    def test_init_Re(self):
        """
        Tests initialization of Recovered compartment.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.5,
            fraction_recovered = 0.35)
        self.assertEqual(np.sum(network.Re), 35)

    def test_reset_Su_In_Re(self):
        """
        Tests reset of compartmental histories.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.5,
            fraction_recovered = 0.35)
        network.In -= network.In
        network.reset_Su_In_Re()
        self.assertEqual(np.sum(network.In), 50)

    def test_generate_random_walk_length(self):
        """
        Tests the length of the generated random walk.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.5,
            fraction_recovered = 0.35)
        walk = network.generate_random_walk(10)
        self.assertEqual(len(walk), 10)

    def test_generate_random_walk_degrees_length(self):
        """
        Tests the length of the generated random degree sequence.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.5,
            fraction_recovered = 0.35)
        walk = network.generate_random_walk_degree_sequence(10)
        self.assertEqual(len(walk), 10)

    def test_immunize_network_vaccinate(self):
        """
        Tests that network immunization is working correctly.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.5,
            fraction_recovered = 0.35)
        Im = copy.deepcopy(network.In)
        np.random.shuffle(Im)
        network.immunize_network(Im, efficacy = 0.7)
        self.assertEqual(np.sum(network.Im), np.sum(Im))

    def test_init_histories(self):
        """
        Tests initiation of simulation history.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.25)
        sim = contagion.Contagion(network, save_history = True)
        self.assertEqual(len(sim.Su_hist), 1)

    def test_run_simulation(self):
        """
        Tests that the simulation runs for an appropriate number of steps.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.25)
        sim = contagion.Contagion(network, save_history = True)
        sim.run_simulation()
        self.assertGreater(len(sim.In_hist), 4)

    def test_max_infected(self):
        """
        Tests believability of maximum infected during simulation.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.25)
        sim = contagion.Contagion(network, save_history = True)
        self.assertGreater(sim.run_simulation_get_max_infected(), 24)

    def test_max_infected_index(self):
        """
        Tests index of maximum infected during simulation.
        """
        G = nx.barabasi_albert_graph(100, 5)
        network = contagion.ContactNetwork(
            G,
            fraction_infected = 0.25)
        sim = contagion.Contagion(network, save_history = True)
        self.assertGreater(sim.run_simulation_get_max_infected_index(), -1)


if __name__ == '__main__':
    unittest.main()
