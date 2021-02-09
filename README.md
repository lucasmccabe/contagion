[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3993314.svg)](https://doi.org/10.5281/zenodo.3993314)
[![PyPI version](https://badge.fury.io/py/contagion.svg)](https://badge.fury.io/py/contagion)
[![Documentation Status](https://readthedocs.org/projects/contagion/badge/?version=latest)](https://contagion.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/lucasmccabe/contagion.svg?branch=master)](https://travis-ci.com/lucasmccabe/contagion)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

# contagion

> `contagion` is a Python package supporting node immunization and network contagion simulation

`contagion` is designed to be easy-to-use and full-featured, supporting computer scientists, public health researchers, network theorists, and more. Here are a few things we love about `contagion`:

- accessible interface for incorporating node immunization into contagion simulations
- supports immunization with delayed effect and variable immunity durations
- handles partial immunity and time-varying transmission rates
- can track symptom onset
- implements node testing policies (random, contact tracing)

![Carbon Snippet](https://raw.githubusercontent.com/lucasmccabe/contagion/master/images/carbon_snippet.png)


## Table of Contents
* [Table of Contents](#table-of-contents)
* [Getting Started](#getting-started)
* [Documentation](#documentation)
* [Example Usage](#example-usage)
* [Citing contagion](#citing-contagion)
* [Contributing to contagion](#contributing-to-contagion)
* [Contact](#contact)
* [Requirements](#requirements)
* [License](#license)


## Getting Started
Install `contagion` with [pip](https://pypi.org/project/contagion/):

```bash
pip install contagion
```

Once `contagion` is installed, import `NetworkX` and `contagion`:

```python
import networkx
from contagion import contagion
```


## Documentation
Official documentation - including a [tutorial](https://contagion.readthedocs.io/en/latest/tutorial.html), [API reference](https://contagion.readthedocs.io/en/latest/apiref.html), and a few worked [examples](https://contagion.readthedocs.io/en/latest/examples.html) - is available on [Read the Docs](https://contagion.readthedocs.io).


## Citing contagion
If you find `contagion` useful in your work, please use the [Zenodo](https://zenodo.org/record/3993314) software citation.


## Requirements
This project was created with:
- `matplotlib==3.3.3`
- `numpy==1.19.3`
- `networkx==2.5`
- `scipy>=1.5.0`
- `seaborn==0.11.1`


## Contributing to contagion

We'd love your help! If you'd like to make an addition or improvement, please submit a [pull request](https://github.com/lucasmccabe/contagion/pulls) consisting of an atomic commit and a brief message describing your contribution. If you find something wrong, please submit a bug report to the [issue tracker](https://github.com/lucasmccabe/contagion/issues). For other questions or comments, feel free to [contact me](#citing-contagion) directly.

Thanks for helping make `contagion` better!


## Contact
- Lucas McCabe ([lucas.mccabe@jhu.edu](mailto:lucas.mccabe@jhu.edu))


## License
[MIT](https://choosealicense.com/licenses/mit/)
