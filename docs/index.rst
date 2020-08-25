.. contagion documentation master file, created by
   sphinx-quickstart on Sun Aug 23 20:21:28 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation for contagion
===========================

.. image:: https://readthedocs.org/projects/contagion/badge/?version=latest
    :target: https://contagion.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

contagion is a Python package supporting agent-based disease simulation on networks.

The code can be found on GitHub_.



General Info
============

contagion consists of two classes:

    - ContactNetwork_ builds upon a networkx_ graph, adding vectors for tracking susceptible, infected, and recovered nodes and providing the ability to initialize with a specified fraction of nodes infected and/or recovered.

    - Contagion_ implements disease simulations on contact networks, providing the ability to retrieve per-step compartmental histories and simulate test procedures (e.g. random testing or contact tracing).



Table of Contents
=================

.. toctree::
   :maxdepth: 3

   installation
   examples
   apiref
   cite



.. _GitHub: https://github.com/lucasmccabe/contagion
.. _networkx: https://github.com/networkx/networkx
.. _ContactNetwork: https://contagion.readthedocs.io/en/latest/apiref_ContactNetwork.html
.. _Contagion: https://contagion.readthedocs.io/en/latest/apiref_Contagion.html#the-contagion-class
