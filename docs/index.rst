.. contagion documentation master file, created by
   sphinx-quickstart on Sun Aug 23 20:21:28 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to contagion's documentation!
=====================================

.. image:: https://readthedocs.org/projects/contagion/badge/?version=latest
    :target: https://contagion.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

contagion is a Python package supporting agent-based disease simulation on networks.


General Info
============

contagion consists of two primary components:

    - ContactNetwork builds upon a networkx_ graph, adding vectors for tracking susceptible, infected, and recovered nodes and providing the ability to initialize with a specified fraction of nodes infected and/or recovered.
    - Contagion implements disease simulations on contact networks, providing the ability to retrieve per-step compartmental histories and simulate test procedures (e.g. random testing or contact tracing).


Table of Contents
=================

.. toctree::
   :maxdepth: 3

   installation
   examples
   apiref
   cite



.. _networkx: https://github.com/networkx/networkx
