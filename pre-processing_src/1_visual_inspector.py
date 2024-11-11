"""
Visually inspect MaNGA images and remose rejected images

rejection criteria:
- image is clearly obstructed by foreground star
- On-going merger events
- Dominated centre with AGN class spaxels
- sparse spatial coverage in the centre and outskirts of the galaxy

"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from astropy.io import fits
import matplotlib as mpl
import argparse
import glob
from matplotlib import colors
import numpy as np


# import config.yaml file
import yaml

with open("/Users/mmckay/phd_projects/breakBRD_radial_profiles_analysis/conf/main.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


mpl.rcParams["figure.dpi"] = 150
# global_df = pd.read_csv(config["data"]["lg12_global_table"])

#! Check visually vetted table
# global_df = pd.read_csv(
#     "/Users/mmckay/phd_projects/breakBRD_radial_profiles_analysis/DATA/GLOBAL_TABLES/vis_vetted_lg12_global.csv")

#! Check rejected table
global_df = pd.read_csv(
    "/Users/mmckay/phd_projects/breakBRD_radial_profiles_analysis/DATA/GLOBAL_TABLES/visual_rejects_global_table.csv")


fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(10, 10))

# Storee reject plateifu's in list when visually inspecting
reject_plateifu_list = []
i = 0
for plateifu in global_df["plateifu"]:
    print(plateifu)
    sdss_img_path = config["data"]["all_sdss_rgb_images_dirpath"] + \
        plateifu + ".png"
    # sdss_img_path = f"{config["data"]["all_sdss_rgb_images_dirpath"]}{plateifu}.png"
    sdss_img_array = mpimg.imread(sdss_img_path)
    # hdu = fits.open(f"{BBRD_IFU_FITS_PATH}{plateifu}_MM.fits")
    hdu = fits.open(config["data"]["lg12_fits_dir"] + plateifu + "_MM.fits")
    # ax0.title(plateifu)
    ax0.imshow(sdss_img_array)

    cmap = colors.ListedColormap(["blue", "green", "red"])
    bounds = [1, 2, 3, 4]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    im = ax1.imshow(
        hdu[55].data, origin="lower", cmap=cmap, norm=norm, interpolation="nearest"
    )
    im2 = ax2.imshow(
        hdu[0].data, origin="lower", cmap='jet', interpolation="nearest")
    ax1.contour(hdu['ELLIP R'].data, levels=np.arange(3, 4, 1), origin='lower', colors='k',
                linewidths=3)
    # ax1.contour(hdu['R/REFF'].data, levels=np.arange(0, 1.5, 0.5), origin='lower', colors='c',
    #             linewidths=3)
    ax1.contour(hdu['R/REFF'].data, levels=np.linspace(0.01, 2.0, 11), origin='lower', colors='c',
                linewidths=3)
    ax2.contour(hdu['ELLIP R'].data, levels=np.arange(3, 4, 1), origin='lower', colors='k',
                linewidths=3)
    ax2.contour(hdu['R/REFF'].data, levels=np.linspace(0.01, 2.0, 11), origin='lower', colors='c',
                linewidths=3)
    cb = plt.colorbar(im2, ax=ax2, orientation="horizontal")
    cbaxes = fig.add_axes([1, 0.1, 0.03, 0.8])
    cbar = fig.colorbar(im, ax=ax2, cax=cbaxes, aspect=5.3,
                        orientation='vertical', extend='both')
    # cbar.ax.tick_params(labelsize=25)
    # cbar.set_label(label='$\sigma_{gas}[km/s]$', size='large', fontsize=20)
    # plt.colorbar(cbar, ax=ax2, cax=cbaxes)
    plt.tight_layout(pad=3)

    # ax1.imshow(hdu[55].data, origin="lower")
    hdu.close()
    plt.tight_layout()
    plt.show(block=False)

    #! Reject image if it is clearly obstructed
    i += 1
    reject_user_input = input(
        "[{}/{}] reject Image?(y/n):".format(i, len(global_df["plateifu"]))
    )
    print(reject_user_input, [plateifu])
    if reject_user_input.lower() == "y":
        reject_plateifu_list.append(plateifu)
        ax1.cla()
        ax2.cla()
    elif reject_user_input.lower() == "n":
        ax1.cla()
        ax2.cla()
        pass
    else:
        print("wrong input, try again")
        ax1.cla()
        ax2.cla()

        pass
    plt.cla()
    cb.remove()


# Make table of visually rejected and vetted plateifu's
print(reject_plateifu_list)
mk_new_csv_user_response = input(
    "Make new csv with noisey data plateifu values removed?(y/n):"
)
# sample_name_user_input = input("Which sample? (csf/cqc/cgv/bbrd):")
if mk_new_csv_user_response == "y":
    # Save table with rejected plateifu's
    reject_global_df = global_df[global_df["plateifu"].isin(
        reject_plateifu_list)]
    reject_global_df.to_csv(
        config["data"]["global_table_dir"] + "visual_rejects_global_table.csv",
        index=False,
    )

    # Save table with visually good images
    clean_global_df = global_df[~global_df["plateifu"].isin(
        reject_plateifu_list)]
    clean_global_df.to_csv(
        config["data"]["global_table_dir"] +
        "vis_vetted_global_table.csv",
        index=False,
    )

else:
    pass
