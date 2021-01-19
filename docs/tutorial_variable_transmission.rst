===========================
Variable Transmission Rates
===========================

It may be desirable for the transmission rate to vary over time. We accomplish this by passing a list of rates to ``omega``. The value of the list at each index represents the transmission rate at the corresponding time-step. If the simulation runs longer than the length ``omega``, the last value of ``omega`` will be used for the remainder of the simulation.

.. code-block:: python

    import networkx
    from contagion import contagion

    G = networkx.barabasi_albert_graph(1000, 25)
    net = contagion.ContactNetwork(G)

    sim = contagion.Contagion(
      net,
      beta = [0.25]*10+[0.75])

In the above code block, the transmission rate is 0.25 for the first 10 time-steps, after which the transmission rate is 0.75.
