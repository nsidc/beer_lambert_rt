<img alt="NSIDC logo" src="https://nsidc.org/themes/custom/nsidc/logo.svg" width="150" />


# A Beer-Lambert Radiative Transfer Model

The code in this repository is a model to calculate under-ice Photosynthetically Active Radiation for the Arctic Ocean.  The code was initially developed and used to estimate under-ice sunlight and phytoplankton bloom time for the Arctic Ocean in Stroeve et al (2021).  That original code has been refactored and updated to improve model run time and maintainability.

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
- `pandas` is also used to load and write data
- `matplotlib` and `cartopy` are used for plotting
- `scipy` is used to estimate snow depth distributions
- `pytest` is used for code testing.


## Installation

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the repository to your GitHub user account.
2. [Clone](https://docs.github.com/en/get-started/quickstart/fork-a-repo#cloning-your-forked-repository) your forked repository to your local machine.  The example below is for HTTPS.  
   `git clone https://github.com/YOUR-USERNAME/beer-lambert-rt`  
   This will create a directory `beer-lambert-rt`
3. `cd beer-lambert-rt`
4. It is recommended to setup a new virtual environment to run the model.
   `conda env create -f environment.yml`
5. Install the package using
   `pip install -e .
   This creates an editable installed version of the `beer_lambert_rt` package.
6. The package is written with tests.  To ensure that the code runs as expected run `pytest` from the command line.
   ```
   $ pytest
   ====================== test session starts ==============================================
   platform linux -- Python 3.10.0, pytest-7.2.1, pluggy-1.0.0
   rootdir: /home/apbarret/src/beer_lambert_rt
   plugins: anyio-3.6.2
   collected 7 items
   
   tests/test_transmission.py .......                                                 [100%]
   
   ===================== 7 passed in 0.13s =================================================
   ```

## Usage

The radiative transfer model can be run within a script or directly from the command line.

### Running from the command line

The command line tool requires a netCDF or csv file that contain ice
thickness, snow depth, pond depth, pond fraction, sea ice
concentration, shortwave surface flux and skin temperature.  The
expected variable names and units are given in table 1 below.

_Add table_

The model is run with the command

```
python run_beer_lambert_rt <file_path>
```

### Running from a script or Jupyter Notebook

The `beer_lambert_rt.model.run_model` function executes the model.
Input parameters can be passed as scalars, `numpy.ndarray` arrays,
`xarray.DataArrays`, or `pandas.Series`.

From a python interpreter or IPython session...

```
# Import the run_model function 
In [1]: from beer_lambert_rt.model import run_model

# Print the docstring
In [2]: run_model?
Signature:
run_model(
    ice_thickness: float,
    snow_depth: float,
    albedo: float,
    sw_radiation: float,
    skin_temperature: float,
    sea_ice_concentration: float,
    pond_depth=0.0,
    pond_fraction=0.0,
    use_distribution=True,
    nsnow_class=7.0,
    max_snow_factor=3.0,
    nice_class=15.0,
    max_ice_factor=3.0,
)
Docstring:
Runs Beer-Lambert RT model

Arguments
---------
:ice_thickness: (float) ice thickness in meters (scalar or array-like)
:snow_depth: (float) snow depth in meters (scalar or array-like)
:albedo: surface albedo [0-1] (scalar or array-like)
:sw_radiation: Shortwave radiation (scalar or array-like)
:skin_temperature: Skin temperature in degrees C (scalar or array-like)
:sea_ice_concentration: Sea ice concentration [0-1] (scalar or array-like).

Keywords
--------
:pond_depth: pond_depth in meters (scalar or array-like). Ignored if None.
:pond_fraction: pond_fraction [0-1] (scalar or array-like). Only used if pond-depth
                is not None. 
:use_distribution: (boolean) Use ice_thickness and snow_depth to define snow and 
                   ice distribution. Default=True,
:nsnow_class: Number of snow classes in snow depth distribution (scalar) Default=7.
:max_snow_factor: Set maximum snow depth in distribution as max_snow_factor*snow_depth
                  Default=3.,
:nice_class: **Not Used** Number of ice classes in ice thickness distribution (scalar) 
             Default=15.
:max_ice_factor: **Not Used** Set maximum ice thickness as max_ice_factor*ice_thickness
                 Default=3.

:returns: TBD but PAR, Flux, ????
File:      ~/src/beer_lambert_rt/beer_lambert_rt/model.py
Type:      function

# Run the model for a single input passed as scalars
In [3]: run_model(1.5, 0.3, 0.8, 100., -5., 1.)
Out[3]: (array([1.18633448]), array([4.15217068]))
```

`run_model` returns short wave radiative flux at the base of the sea
ice and the flux expressed as Photosynthetically Active Radiation
(PAR).

See `run_beer_lambert_rt.ipynb` Jupyter Notebook in the `notebooks`
directory for further examples of running the model interactively.


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
