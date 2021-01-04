==========================
Tutorial: Contact Networks
==========================


contagion simulations run on ContactNetwork_ objects. To begin, create a NetworkX graph and initialize a ContactNetwork around it:

.. code-block:: python

    import networkx
    from contagion import contagion

    G = networkx.barabasi_albert_graph(1000, 25)
    net = contagion.ContactNetwork(G)


To specify a portion of the network to be (randomly) infected and/or recovered at initialization, simply pass the desired value(s) into the ``fraction_infected`` and/or ``fraction_recovered`` parameters, respectively:

.. code-block:: python

  net = contagion.ContactNetwork(
    G,
    fraction_infected = 0.1,
    fraction_recovered = 0.)


To retrieve the ContactNetwork's size (number of nodes), undelying NetworkX graph, or adjacency matrix, use the ``n``, ``G``, or ``A`` attributes, respectively.


If you are interested in immunizing your network using a specific policy, proceed to the immunization_ part of the tutorial. Otherwise, proceed to the simulation_ section.






.. _ContactNetwork: https://contagion.readthedocs.io/en/latest/apiref_ContactNetwork.html
.. _NetworkX: https://networkx.org
.. _immunization: https://contagion.readthedocs.io/en/latest/tutorial_Immunization.html
.. _simulation: https://contagion.readthedocs.io/en/latest/tutorial_simulation.html
