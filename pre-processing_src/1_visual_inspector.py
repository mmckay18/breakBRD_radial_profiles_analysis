import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from astropy.io import fits
import matplotlib as mpl
import argparse
import glob
from matplotlib import colors


# import config.yaml file
import yaml

with open("/Users/mmckay/phd_projects/breakBRD/conf/main.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


mpl.rcParams["figure.dpi"] = 150
global_df = pd.read_csv(config["data"]["lg12_global_table"])

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 10))

# Storee reject plateifu's in list when visually inspecting
reject_plateifu_list = []
i = 0
for plateifu in global_df["plateifu"]:
    print(plateifu)
    sdss_img_path = config["data"]["all_sdss_rgb_images_dirpath"] + plateifu + ".png"
    # sdss_img_path = f"{config["data"]["all_sdss_rgb_images_dirpath"]}{plateifu}.png"
    sdss_img_array = mpimg.imread(sdss_img_path)
    # hdu = fits.open(f"{BBRD_IFU_FITS_PATH}{plateifu}_MM.fits")
    hdu = fits.open(config["data"]["lg12_fits_dir"] + plateifu + "_MM.fits")
    # ax0.title(plateifu)
    ax0.imshow(sdss_img_array)
    hdu.close()

    cmap = colors.ListedColormap(["blue", "green", "red"])
    bounds = [1, 2, 3, 4]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    im = ax1.imshow(
        hdu[55].data, origin="lower", cmap=cmap, norm=norm, interpolation="nearest"
    )
    # ax1.imshow(hdu[55].data, origin="lower")
    plt.show(block=False)
    # plt.pause(1)
    # input("Press enter to continue...")

    #! Reject image if it is clearly obstructed
    i += 1
    reject_user_input = input(
        "[{}/{}]  reject Image?(y/n):".format(i, len(global_df["plateifu"]))
    )
    print(reject_user_input, [plateifu])
    if reject_user_input.lower() == "y":
        reject_plateifu_list.append(plateifu)
        plt.cla()
    elif reject_user_input.lower() == "n":
        plt.cla()
        pass
    else:
        print("wrong input, try again")
        plt.cla()
        continue


# Make table of visually rejected and vetted plateifu's
print(reject_plateifu_list)
mk_new_csv_user_response = input(
    "Make new csv with noisey data plateifu values removed?(y/n):"
)
# sample_name_user_input = input("Which sample? (csf/cqc/cgv/bbrd):")
if mk_new_csv_user_response == "y":
    # Save table with rejected plateifu's
    reject_global_df = global_df[global_df["plateifu"].isin(reject_plateifu_list)]
    reject_global_df.to_csv(
        config["data"]["global_table_dir"] + "visual_rejects_global_table.csv",
        index=False,
    )

    # Save table with visually good images
    clean_global_df = global_df[~global_df["plateifu"].isin(reject_plateifu_list)]
    reject_global_df.to_csv(
        config["data"]["global_table_dir"] + "visually_vetted_global_table.csv",
        index=False,
    )

else:
    pass
