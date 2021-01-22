==================================================
Loss of immunity for immunized and recovered nodes
==================================================


Here, we immunize the 500 nodes with highest eigenvector centrality, using a vaccine with 90% efficacy. We also apply different immunity-loss probabilities to vaccinated nodes (0.1) and naturally-recovered nodes (0.01).

.. code-block:: python

    import networkx as nx
    from contagion import contagion

    network = contagion.ContactNetwork(
        nx.barabasi_albert_graph(1000, 5))

    immunization = contagion.Immunization(network)
    Im_array = immunization.generate_centrality_immunization_array(
        Q = 500,
        centrality_type='eigenvector',
        order='highest')

    network.immunize_network(
        Im = Im_array,
        im_type = "vaccinate",
        im_starts_after = 5,
        efficacy = 0.9)

    sim = contagion.Contagion(
        network = network,
        beta = 0.15,
        gamma = 0.05,
        omega = (0.01, 0.1))

    sim.plot_simulation(steps = 50)


.. image:: /_static/ex4.png
