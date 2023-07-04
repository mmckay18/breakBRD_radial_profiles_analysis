import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from astropy.io import fits
import glob
import numpy as np

import yaml

with open("/Users/mmckay/phd_projects/breakBRD/conf/main.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def freq_weighted_median(supercsv_df, x_col, y_col, yerr=None, radial_bins=np.linspace(0.01, 2.2, 11)):
    """
    Calaclates the frequency weighted median for each radial bin using the concatentaed dataframe (supercsv)
    - Data should already be  vetted and cleaned and the supercsv file should be made before processing running this script
    """

    xdata = supercsv_df[x_col]
    ydata = supercsv_df[y_col]
    if yerr is not None:
        yerr = supercsv_df[yerr]
    else:
        pass

    # Start binning
    digitized = np.digitize(xdata, radial_bins)
    print(digitized)

    bbrd_weight_df = pd.DataFrame()
    # Create a CSV to store all the weights and averages of a bin for each galaxy
    bbrd_weighted_avgs_df = pd.DataFrame()

    # Empty list to store weights  and weights*avg values
    ydata_bin_weight_list = []
    ydata_wts_avg_per_bin_list = []

    for bin in range(1, len(radial_bins)):
        ydata_bin_spax = ydata[digitized == bin]
        # print(
        #     f'xdata column {len(xdata_bin_spax)}, ydata column {len(ydata_bin_spax)}')
        # ydata_bin_weight_list.append(len(ydata_bin_spax))
        ydata_wts_avg_per_bin_list.append(
            np.nanmean(ydata_bin_spax) * len(ydata_bin_spax))
        ydata_wts_avg_per_bin_list.append(
            np.nanmedian(ydata_bin_spax) * len(ydata_bin_spax))

        # # Appends weights to a dataframe
        # bbrd_weight_df[csv_file_path[-19:]] = ydata_bin_weight_list
        # bbrd_weighted_avgs_df[csv_file_path[-19:]] = ydata_wts_avg_per_bin_list

    # # Adds the total number of spaxels in a bin (Denominator)
    # bbrd_weight_df["Total # spaxels in bin"] = bbrd_weight_df.sum(axis=1)

    # # Sums of all the weights (Numerator)
    # # bbrd_weighted_avgs_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    # bbrd_weighted_avgs_df["Sum of w*avg in bin"] = bbrd_weighted_avgs_df.sum(axis=1)

    # # weighted_average radial profile
    # bbrd_ydata_w_avgs = (
    #     bbrd_weighted_avgs_df["Sum of w*avg in bin"]
    #     / bbrd_weight_df["Total # spaxels in bin"]
    # )
    # xdata_bin_spax = [xdata[digitized == i].max() for i in range(1, len(radial_bins))]


if __name__ == "__main__":

    supercsv_df = pd.read_csv(config["data"]["bbrd_supercsv"])
    print(supercsv_df.plateifu.unique())
    freq_weighted_median(supercsv_df, x_col='R/REFF', y_col='GYR_LW',
                         yerr=None, radial_bins=np.linspace(0.01, 2.2, 11))
