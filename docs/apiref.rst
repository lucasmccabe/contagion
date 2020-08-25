=============
API Reference
=============


.. currentmodule:: contagion

.. autosummary:: contagion



contagion consists of two classes:

    - ContactNetwork_ builds upon a networkx_ graph, adding vectors for tracking susceptible, infected, and recovered nodes and providing the ability to initialize with a specified fraction of nodes infected and/or recovered.
    - Contagion_ implements disease simulations on contact networks, providing the ability to retrieve per-step compartmental histories and simulate test procedures (e.g. random testing or contact tracing).



Contents
-----------------

.. toctree::
   :maxdepth: 3

   apiref_ContactNetwork
   apiref_Contagion



.. _ContactNetwork: https://contagion.readthedocs.io/en/latest/apiref_ContactNetwork.html
.. _Contagion: https://contagion.readthedocs.io/en/latest/apiref_Contagion.html#the-contagion-class
