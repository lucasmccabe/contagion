[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3993314.svg)](https://doi.org/10.5281/zenodo.3993314)
[![PyPI version](https://badge.fury.io/py/contagion.svg)](https://badge.fury.io/py/contagion)
[![Documentation Status](https://readthedocs.org/projects/contagion/badge/?version=latest)](https://contagion.readthedocs.io/en/latest/?badge=latest)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

# contagion

> `contagion` is a Python package supporting agent-based disease simulation on networks.


## Table of Contents
* [Table of Contents](#table-of-contents)
* [Documentation](#documentation)
* [Installation](#installation)
* [Example Usage](#example-usage)
* [Citing contagion](#citing-contagion)
* [Contact](#contact)
* [Requirements](#requirements)
* [License](#license)


## Documentation
The official documentation is available on [Read the Docs](https://contagion.readthedocs.io).

## Installation
We can install `contagion` with [pip](https://pypi.org/project/contagion/):

```bash
pip install contagion
```

Once `contagion` is installed, import `networkx` and `contagion`:

```python
import networkx
from contagion import contagion
```

## Example Usage
We can initialize a `ContactNetwork` using any `networkx` graph:

```python
G = networkx.barabasi_albert_graph(1000, 25)
network = contagion.ContactNetwork(G, fraction_infected = 0.01)
```

Once a `ContactNetwork` is initialized, we can run a disease simulation. For this example, we'll also differentiate between symptomatic and asymptomatic infections:

```python
sim = contagion.Contagion(
    network = network,
    beta = 0.2,
    gamma = 0.1,
    track_symptomatic = True,
    psi = 0.2)
sim.plot_simulation(steps = 100)
```

which produces the following simple compartmental history plot:

![Sample Simulation Compartmental Histories with Symptomatic Tracking](https://raw.githubusercontent.com/lucasmccabe/contagion/dev/images/Sample%20Simulation%20Compartmental%20Histories%20with%20Symptomatic%20Tracking.png)


Additional examples are found [here](https://contagion.readthedocs.io/en/latest/examples.html).

## Citing contagion
If you find `contagion` useful in your work, please use the [Zenodo](https://zenodo.org/record/3993314) software citation.

## Contact
- Lucas McCabe ([lucas.mccabe@jhu.edu](mailto:lucas.mccabe@jhu.edu))

## Requirements
This project was created with:
- `matplotlib==3.2.1`
- `numpy==1.16.6`
- `networkx==2.4`
- `seaborn==0.8.1`

## License
[MIT](https://choosealicense.com/licenses/mit/)
