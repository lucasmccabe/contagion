============
Tutorial: Immunization
============

If you haven't initialized your ContactNetwork, it's best to go back to the ContactNetwork_ section of the tutorial.

Immunization is done using NumPy_ arrays. Immunization arrays are column vectors of the same x-dimension as the ContactNetwork's adjacency matrix, as elements of the immunization array correspond to rows of the adjacency matrix.

If you want to use one of our built-in baseline methods for immunization, initialize an Immunization object and select the algorithm you'd like to try, providing an integer Q for the number of immunization units to allocate:

.. code-block:: python

    import networkx
    from contagion import contagion

    G = networkx.barabasi_albert_graph(1000, 25)
    net = contagion.ContactNetwork(G)

    Im = contagion.Immunization(net).generate_random_immunization_array(Q = 20)


The above creates a binary immunization array, indicating that node i is to be immunized if Im[i] == 1. The method generate_random_immunization_array() allocates the Q=20 units randomly across the array, but we also provide methods for using degree or centrality-based heuristics (more information here_). Alternately, you can use any binary NumPy array that represents the algorithm of your choice.

Once you have an immunization array, use ContactNetwork's ``immunize_network`` method to apply your policy to the network:

.. code-block:: python

  net.immunize_network(
    Im,
    im_type = "vaccinate",
    im_starts_after = 5,
    efficacy = 0.9)


contagion supports two types of node immunization (``im_type``). The default type is "vaccinate" (illustrated above), which protects nodes against transmission at a given efficacy level (default is 100% efficacy). A user may wish to delay immunization until a later step in the contagion simulation. This can be done using the ``im_starts_after`` parameter, which dictates the simulation step after which the immunization array will apply.

The second type of immunization is "monitor," which treats "immunization" like sensor placement for outbreak detection. Nodes are not protected against transmission, but are tracked so that the simulation stops when ``mo_thresh`` monitored nodes have been infected:

.. code-block:: python

  net.immunize_network(
    Im,
    im_type = "monitor",
    mo_thresh = 20)


If you'd like to run a contagion simulation on your network, proceed to the simulation_ section.





.. _ContactNetwork: https://contagion.readthedocs.io/en/latest/tutorial_ContactNetwork.html
.. _NumPy: https://numpy.org/doc/stable/index.html
.. _here: https://contagion.readthedocs.io/en/latest/apiref_Immunization.html
.. _simulation: https://contagion.readthedocs.io/en/latest/tutorial_simulation.html
