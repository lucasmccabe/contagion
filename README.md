# contagion

## Introduction
`contagion` is a Python package supporting agent-based disease simulation on networks.

## Table of Contents
* [Introduction](#introduction)
* [Table of Contents](#table-of-contents)
* [General Info](#general-info)
* [Installation](#installation)
* [Usage](#usage)
* [Requirements](#requirements)
* [License](#license)

## General Info
`contagion` consists of two primary components:
- `ContactNetwork` builds upon a networkx graph, adding vectors for tracking susceptible, infected, and recovered nodes and providing the ability to initialize with a specified fraction of nodes infected and/or recovered.
- `Contagion` implements disease simulations on contact networks, providing the ability to retrieve per-step compartmental histories and simulate test procedures (e.g. random testing or contact tracing).

## Installation
In the future, we'll use [pip](https://pip.pypa.io/en/stable/) to install `contagion` (but not yet):

```bash
pip install contagion
```

Once `contagion` is installed, import `networkx` and `contagion`:

```python
import networkx
from contagion import contagion
```

## Usage
We can initialize a `ContactNetwork` using any `networkx` graph:

```python
G = networkx.barabasi_albert_graph(1000, 25)
network = contagion.ContactNetwork(G, fraction_infected = 0.01)
```

Once a `ContactNetwork` is initialized, we can run a disease simulation:

```python
sim = contagion.Contagion(network = network, beta = 0.2, gamma = 0.1)
sim.plot_simulation(steps = 100)
```

which produces the following simple compartmental history plot:

![Sample Simulation Compartmental Histories](images\Sample Simulation Compartmental Histories.png)

## Requirements
This project was created with:
- `matplotlib==3.2.1`
- `numpy==1.16.6`
- `networkx==2.4`
- `seaborn==0.8.1`

## License
[MIT](https://choosealicense.com/licenses/mit/)
