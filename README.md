<img alt="NSIDC logo" src="https://nsidc.org/themes/custom/nsidc/logo.svg" width="150" />


# A Beer-Lambert Radiative Transfer Model

The code in this repository was used to calculate under-ice Photosynthetically Active Radiation for the Arctic Ocean.

The code was used in Stroeve et al (2021)

Stroeve J, Vancoppenolle M, Veyssiere G, Lebrun M, Castellani G, Babin M, Karcher M, Landy J, Liston GE and Wilkinson J (2021) A Multi-Sensor and Modeling Approach for Mapping Light Under Sea Ice During the Ice-Growth Season. Front. Mar. Sci. 7:592337. [doi: 10.3389/fmars.2020.592337](https://www.frontiersin.org/articles/10.3389/fmars.2020.592337/full)


## Level of Support

* This repository is not actively supported by NSIDC but we welcome issue submissions and
  pull requests in order to foster community contribution.

See the [LICENSE](LICENSE) for details on permissions and warranties. Please contact
nsidc@nsidc.org for more information.


## Requirements

The package requires python 3.10 or later.

Imported dependences are listed in `environment.yml`.

- `numpy` is used for model calculations
- `xarray` is used to load and write data
- `matplotlib` and `cartopy` are used for plotting
- `pytest` is used for code testing.


## Installation

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the repository to your GitHub user account.
2. [Clone](https://docs.github.com/en/get-started/quickstart/fork-a-repo#cloning-your-forked-repository) your forked repository to your local machine.  The example below is for HTTPS.
   `git clone https://github.com/YOUR-USERNAME/beer-lambert-rt`
   This will create a directory `beer-lambert-rt`
3. `cd beer-lambert-rt`
4. It is recommended to setup a new virtual environment to run the model.
   `conda env create -f environment.yml`
5. The package is written with tests.  To ensure that the code runs as expected run `pytest` from the command line.
   ```
   $ pytest
   =========================================================================================== test session starts ===========================================================================================
platform linux -- Python 3.10.0, pytest-7.2.1, pluggy-1.0.0
rootdir: /home/apbarret/src/beer_lambert_rt
plugins: anyio-3.6.2
collected 7 items                                                                                                                                                                                         

tests/test_transmission.py .......                                                                                                                                                                  [100%]

============================================================================================ 7 passed in 0.13s ============================================================================================
   ```

## Usage

{usage}: Describe how to use this software, with platform-specific instructions
      if necessary.

## Contributing
We welcome issues and pull requests.  See the [contributing guide]() to contribute.


## Troubleshooting

{troubleshooting}: Describe any tips or tricks in case the user runs into
      problems.


## License

See [LICENSE](LICENSE).


## Code of Conduct

See [Code of Conduct](CODE_OF_CONDUCT.md).


## Credit

This work resulted from the NERC project (NE/R012725/1), known as EcoLight, part of the Changing Arctic Ocean programme, jointly funded by the UKRI Natural Environment Research Council (NERC) and the German Federal Ministry of Education and Research (BMBF). JS and GL were also funded under NASA NNX16AK85G. JL was funded under NERC Diatom-ARCTIC (NE/R012849/1). JS was also partially funded under the Canada 150 Chair Program and NASA Grant 80NSSC20K1121.
