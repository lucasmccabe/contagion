=====================
Durations of Immunity
=====================

Immunity durations are implemented probabilistically; rather than provide a fixed number of time-steps for which immunity may last, the user provides a per-step probability (``omega``, defaults to 0) that immune (either immunized or recovered) nodes become susceptible again:

.. code-block:: python

    sim = contagion.Contagion(
      net,
      beta = 0.75,
      omega = 0.05)

If a single value is passed for ``omega``, it will be interpreted as the per-step probability of a recovered node becoming susceptible again.

If a tuple (must be of length 2) is provided, the first element will be interpreted as the per-step probability of a recovered node becoming susceptible again, and the second element will be interpreted as the per-step probability of an immunized node becoming susceptible:

.. code-block:: python

    sim = contagion.Contagion(
      net,
      beta = 0.75,
      omega = (0.1, 0.05))
