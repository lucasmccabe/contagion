===========================
Immunizing a ContactNetwork
===========================

If you haven't defined your immunization strategy, it's best to go back to that_ section of the tutorial.

Once you have an immunization array, use ContactNetwork's ``immunize_network`` method to apply your policy to the network:

.. code-block:: python

  net.immunize_network(
    Im,
    im_type = "vaccinate",
    im_starts_after = 5,
    efficacy = 0.9)


``contagion`` supports two types of node immunization (``im_type``). The default type is "vaccinate" (illustrated above), which protects nodes against transmission at a given efficacy level (default is 100% efficacy).

A user may wish to delay immunization until a later step in the contagion simulation. This can be done using ``im_starts_after``, which dictates the simulation step after which the immunization array will apply.

Immunity may not always last forever, and we take this into account here_.

For other types of immunization, proceed to monitoring_. If you'd like to run a contagion simulation on your network, proceed to the simulation_ section.





.. _that: https://contagion.readthedocs.io/en/latest/tutorial_immunization_policies.html
.. _monitoring: https://contagion.readthedocs.io/en/latest/tutorial_immunization_monitoring.html
.. _here: https://contagion.readthedocs.io/en/latest/tutorial_immunity_duration.html
.. _simulation: https://contagion.readthedocs.io/en/latest/tutorial_simulation.html
