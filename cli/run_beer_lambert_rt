"""CLI to run the Beer Lambert RT model"""

from beer_lambert_rt.model import run_model
import beer_lambert_rt.io as io  #test_datapath, load_data, make_netcdf, make_outpath


def main(outformat="nc", test_format='nc', use_distribution=True):
    """Currently code to run model with dummy data

    Move data to inside run_model
    Enable input of scalar values from command line
    """

    # For testing
    input_file = io.test_datapath(test_format)
    data = io.load_data(input_file)
    
    flux, par = run_model(
        data.ice_thickness,
        data.snow_depth,
        data.albedo,
        data.sw_radiation,
        data.surface_temperature,
        data.sea_ice_concentration,
        use_distribution=use_distribution
    )

    if outformat == 'nc':
        result = io.make_netcdf(flux, par, data.dims, data.coords, input_file)
    elif outformat == 'csv':
        raise NotImplementedError()
    else:
        raise ValueError("Unknown output format")

    outpath = io.make_outpath(input_file, outformat)
    print(outpath)
    
    print(result)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Runs Beer Lambert RT model")
    parser.add_argument("--format", "-f", type=str, default="nc")
    parser.add_argument("--no_distribution", action='store_false')
    parser.add_argument("--output_format", "-of", type=str, default="nc",
                        help="Format of output file (default is netcdf - recommended)")
        
    args = parser.parse_args()
#    print(args)
    
    main(outformat=args.output_format, test_format=args.format,
         use_distribution=args.no_distribution)
