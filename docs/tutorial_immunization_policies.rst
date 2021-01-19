================================
Immunization Arrays and Policies
================================

If you haven't initialized your ContactNetwork, it's best to go back to the ContactNetwork_ section of the tutorial.

Immunization is implemented using NumPy_ arrays. Immunization arrays are column vectors of the same x-dimension as the ContactNetwork's adjacency matrix, as elements of the immunization array correspond to rows of the adjacency matrix.

If you want to use one of our built-in baseline methods for immunization, initialize an Immunization object and select the algorithm you'd like to try, providing an stock level ``Q`` for the number of immunization units to allocate:

.. code-block:: python

    import networkx
    from contagion import contagion

    G = networkx.barabasi_albert_graph(1000, 25)
    net = contagion.ContactNetwork(G)

    Im = contagion.Immunization(net).generate_random_immunization_array(Q = 20)


The above creates a binary immunization array, indicating that node ``i`` is to be immunized if ``Im[i] == 1``. The method ``generate_random_immunization_array()`` allocates the Q=20 units randomly across the array, but we also provide heuristic-based methods, such as degree, centrality, clique, search, and more (more information_). Alternately, you can use any binary NumPy array that represents the algorithm of your choice.

Once you have defined an immunization array, proceed here_ to apply your policy to the network.





.. _ContactNetwork: https://contagion.readthedocs.io/en/latest/tutorial_ContactNetwork.html
.. _NumPy: https://numpy.org/doc/stable/index.html
.. _information: https://contagion.readthedocs.io/en/latest/apiref_Immunization.html
.. _here: https://contagion.readthedocs.io/en/latest/tutorial_immunization.html
