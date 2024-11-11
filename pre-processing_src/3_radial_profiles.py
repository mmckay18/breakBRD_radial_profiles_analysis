import yaml
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from astropy.io import fits
import glob
import numpy as np

sns.set(style="ticks", context="talk")
plt.style.use("seaborn-dark")

# import config.yaml file

with open("/Users/mmckay/phd_projects/breakBRD/conf/main.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def radial_profile(plateifu, xdata, ydata, ydata_err, radial_bins_list):
    """
    computes individual radial profiles for each galaxy in the BBRD and LG12 sample.
    """
    # Read in the csv file for each galaxy
    ifu_csv_df = pd.read_csv(
        config["data"]["all_csv_dir"] + plateifu + "_map.csv")
    #! Drop nans xdata and ydata columns
    ifu_csv_df.dropna(subset=[xdata, ydata, ydata_err], inplace=True)

    # Bin xdata and ydata into even radial_bins_list of R/Reff
    digitized = np.digitize(ifu_csv_df[xdata], radial_bins_list)
    # radial bins xdata
    xval_radial_profile = [
        ifu_csv_df[xdata][digitized == i].max() for i in range(1, len(radial_bins_list))
    ]
    # radial profile ydata
    yval_radial_profile = [
        np.nanmedian(ifu_csv_df[ydata][digitized == i])
        for i in range(1, len(radial_bins_list))
    ]
    for value in yval_radial_profile:
        if value == 0.0 or value == np.inf or value == -np.inf:
            value = np.nan
        else:
            pass

    # Error binning into even radial_bins_list of R/Reff
    # yval_err_radial_profile = [
    #     np.nanmedian(ifu_csv_df[ydata_err][digitized == i])
    #     for i in range(1, len(radial_bins_list))
    # ]
    print(
        f"\tplateifu: {[plateifu]} \n yvalue: {yval_radial_profile} \n xvalue:{xval_radial_profile}"
    )

    return (
        # ifu_csv_df[xdata],
        # ifu_csv_df[ydata],
        # ifu_csv_df[ydata_err],
        yval_radial_profile,
        xval_radial_profile,
        # yval_err_radial_profile,
        # ifu_csv_df.copy(),
    )


if __name__ == "__main__":

    # anything that happens to the LG12 must happen with BBRD!
    df = pd.read_csv(config["data"]["bbrd_supercsv"])
    numeric_columns = df.select_dtypes(include=["float", "int"]).columns
    # print(numeric_columns)

    # global with plateifu column form yaml config file
    tables = [
        "csf_global_table",
        "cgv_global_table",
        "cqc_global_table",
        "lg12_global_table",
        "bbrd_global_table",
        '11_bbrd_global_table'
    ]
    # Itterate through each column and make a radial profile table
    for t in tables:
        print(t)
        samp = t.split("_")[0]
        plateifu_list = pd.read_csv(config["data"][t]).plateifu
        radial_profile_df = pd.DataFrame(
            index=plateifu_list, columns=numeric_columns)
        xdata = "R/REFF"
        radial_bins_list = np.linspace(0.01, 2.0, 10)
        ydata_err = "GYR_ERR"

        for plateifu in plateifu_list:
            for ydata in numeric_columns:
                yval_radial_profile, xval_radial_profile = radial_profile(
                    plateifu, xdata, ydata, ydata_err, radial_bins_list
                )
                try:
                    radial_profile_df.at[plateifu, ydata] = yval_radial_profile
                    radial_profile_df.at[plateifu, xdata] = xval_radial_profile
                except ValueError:
                    print(f"ValueError: {ydata} not in radial_profile_df")
                    pass

        print(radial_profile_df.head(3))
        radial_profile_df.to_csv(
            path_or_buf=config["data"]["radial_profiles_dir"]
            + samp
            + "_radial_profiles.csv"
        )
