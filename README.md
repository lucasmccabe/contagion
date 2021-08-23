[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3993314.svg)](https://doi.org/10.5281/zenodo.3993314)
[![PyPI version](https://badge.fury.io/py/contagion.svg)](https://badge.fury.io/py/contagion)
[![Documentation Status](https://readthedocs.org/projects/contagion/badge/?version=latest)](https://contagion.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/lucasmccabe/contagion.svg?branch=master)](https://travis-ci.com/lucasmccabe/contagion)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

# contagion

> `contagion` is a Python package for node immunization and network contagion simulation.

![Carbon Snippet](https://raw.githubusercontent.com/lucasmccabe/contagion/master/images/carbon_snippet.png)


Here are a few things we love about `contagion`:

- accessible interface for incorporating node immunization into contagion simulations
- supports immunization with delayed effect and variable immunity durations
- handles partial immunity and time-varying transmission rates
- can track symptom onset
- implements node testing policies (random, contact tracing)


## Table of Contents
* [Table of Contents](#table-of-contents)
* [Getting Started](#getting-started)
* [Documentation](#documentation)
* [Example Usage](#example-usage)
* [Contributing to contagion](#contributing-to-contagion)
* [Contact](#contact)
* [Citing contagion](#citing-contagion)
* [Requirements](#requirements)
* [License](#license)


## Getting Started
Install `contagion` with [pip](https://pypi.org/project/contagion/):

```bash
pip install contagion
```


## Documentation
Official documentation - including a [tutorial](https://contagion.readthedocs.io/en/latest/tutorial.html), [API reference](https://contagion.readthedocs.io/en/latest/apiref.html), and a few worked [examples](https://contagion.readthedocs.io/en/latest/examples.html) - is available on [Read the Docs](https://contagion.readthedocs.io).


## Requirements
This project was created with:
- `matplotlib==3.3.3`
- `numpy==1.19.3`
- `networkx==2.5`
- `scipy>=1.5.0`
- `seaborn==0.11.1`


## Contributing to contagion

We'd love your help! If you'd like to make an addition or improvement, please submit a [pull request](https://github.com/lucasmccabe/contagion/pulls) consisting of an atomic commit and a brief message describing your contribution. If you find something wrong, please submit a bug report to the [issue tracker](https://github.com/lucasmccabe/contagion/issues). For other questions or comments, feel free to [contact me](#contact) directly.


## Contact
- Lucas Hurley McCabe ([email](mailto:lucasmccabe@gwu.edu))


## Citing contagion
If you find `contagion` useful in your work, please use the [Zenodo](https://zenodo.org/record/3993314) software citation:

```bash
@software{lucas_mccabe_2021_4456181,
  author       = {Lucas McCabe},
  title        = {lucasmccabe/contagion: v1.3.3},
  month        = jan,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {v1.3.3},
  doi          = {10.5281/zenodo.4456181},
  url          = {https://doi.org/10.5281/zenodo.4456181}
}
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
