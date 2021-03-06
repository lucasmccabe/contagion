==================
Testing Procedures
==================

If you haven't initialized your ContactNetwork, it's best to go back to the ContactNetwork_ section of the tutorial. If you'd like to start by immunizing your network, feel free to go back to the Immunization_ section of the tutorial.


The ``Contagion`` object supports testing procedures by passing ``implement_testing = True`` and a specified ``test_rate`` (dictating the portion(s) of nodes from the network to be tested at each step) at initialization. By default, testing is random:

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
.. _here: https://contagion.readthedocs.io/en/latest/tutorial_simulation_testing.html
