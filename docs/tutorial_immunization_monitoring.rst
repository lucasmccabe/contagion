===============================
Outbreak Detection (Monitoring)
===============================


The second type of immunization is "monitor," which treats "immunization" like sensor placement for outbreak detection. Nodes are not protected against transmission, but are tracked so that the simulation stops when ``mo_thresh`` monitored nodes have been infected:


.. code-block:: python

  net.immunize_network(
    Im,
    im_type = "monitor",
    mo_thresh = 20)


If you'd like to run a contagion simulation on your network, proceed to the simulation_ section.





.. _simulation: https://contagion.readthedocs.io/en/latest/tutorial_simulation.html
