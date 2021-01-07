====================
Tutorial: Simulation
====================

If you haven't initialized your ContactNetwork, it's best to go back to the ContactNetwork_ section of the tutorial. If you'd like to start by immunizing your network, feel free to go back to the Immunization_ section of the tutorial.

If you already have your ContactNetwork, simply create a Contagion object with your desired "virus" transmission rate (``beta``, defaults to 1) and recovery rate (``gamma``, defaults to 1):

.. code-block:: python

    import networkx
    from contagion import contagion

    G = networkx.barabasi_albert_graph(1000, 25)
    net = contagion.ContactNetwork(G)

    sim = contagion.Contagion(
      net,
      beta = 0.75,
      gamma = 0.2)


Optionally, you can track symptom development by turning symptom tracking on and providing a symptom development rate (``psi``, defaults to 1):


.. code-block:: python

    sim = contagion.Contagion(
      net,
      beta = 0.75,
      gamma = 0.2,
      track_symptomatic = True,
      psi = 0.4)


The basic simulation method will run until the "virus" either dies out or encompasses the full network:


.. code-block:: python

    sim.run_simulation()


The user can retrieve the per-step counts of susceptible, infected, and recovered nodes using the ``sim.Su_hist``, ``sim.In_hist``, and ``sim.Re_hist`` attributes, respectively.

For convenience, there are other ways to run the simulation. ``sim.run_simulation_get_max_infected()`` will run and return the maximum number of infected individuals there were at any step. ``sim.run_simulation_get_max_infected_index()`` will run and return the simulation step at which the number of infected individuals peaked. If you've immunized your network using ``im_type = "monitor"``, ``sim.run_simulation_monitor_notification()`` will run up to the point that the threshold number of monitored individuals are infected.

Additionally, the Contagion object supports testing procedures by passing ``implement_testing = True`` and a specified ``test_rate`` (dictating the portion(s) of nodes from the network to be tested at each step) at initialization. By default, testing is random:

.. code-block:: python

    sim = contagion.Contagion(
      net,
      beta = 0.75,
      implement_testing = True,
      test_rate = 0.05)


Testing is assumed to be 100% accurate, revealing whether a node is infected. Re-testing is permitted.

Symptomatic individuals may be more likely to seek testing than asymptomatic individuals. Passing a tuple of length 2 for the ``test_rate`` will designate separate rates for asymptomatic and symptomatic nodes, respectively:


.. code-block:: python

    sim = contagion.Contagion(
      net,
      beta = 0.75,
      implement_testing = True,
      test_rate = (0.01, 0.1))


Alternately, a contact tracing approach is available:

.. code-block:: python

    sim = contagion.Contagion(
      net,
      beta = 0.75,
      implement_testing = True,
      testing_type = "contact",
      test_rate = 0.05)


This method implements the logic illustrated below:

.. image:: /_static/contagiontestandtrace.PNG


.. _ContactNetwork: https://contagion.readthedocs.io/en/latest/tutorial_ContactNetwork.html
.. _Immunization: https://contagion.readthedocs.io/en/latest/tutorial_Immunization.html
.. _Contagion: https://contagion.readthedocs.io/en/latest/apiref_Contagion.html
