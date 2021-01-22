===============================
Time-varying transmission rates
===============================


In this example, the transmission rate is 0.3 for the first 5 time-steps, 0 for the next 10, and 0.3 again for the remainder of the simulation. We also specify the probability of post-recovery immunity loss (`omega = 0.01`).


.. code-block:: python

    import networkx as nx
    from contagion import contagion

    network = contagion.ContactNetwork(
        nx.barabasi_albert_graph(1000, 5))

    sim = contagion.Contagion(
        network = network,
        beta = [0.3]*5+[0]*10+[0.3],
        omega = 0.01,
        gamma = 0.1)

    sim.plot_simulation(steps = 50)


.. image:: /_static/ex3.png
