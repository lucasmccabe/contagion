=============
Example Usage
=============



Example 1: A basic simulation
_____________________________


.. code-block:: python

    import networkx
    from contagion import contagion

    G = networkx.barabasi_albert_graph(1000, 25)
    network = contagion.ContactNetwork(G, fraction_infected = 0.01)

    sim = contagion.Contagion(
        network = network,
        beta = 0.2,
        gamma = 0.1)
    sim.plot_simulation(steps = 100)


.. image:: /_static/ex1.png
