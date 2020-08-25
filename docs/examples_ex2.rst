=============
Example Usage
=============



Example 2: Differentiating between symptomatic and asymptomatic infections
__________________________________________________________________________


.. code-block:: python

    import networkx
    from contagion import contagion

    G = networkx.barabasi_albert_graph(1000, 25)
    network = contagion.ContactNetwork(G, fraction_infected = 0.01)

    sim = contagion.Contagion(
        network = network,
        beta = 0.2,
        gamma = 0.1,
        track_symptomatic = True,
        psi = 0.2)
    sim.plot_simulation(steps = 100)


.. image:: /_static/ex2.png
