import yaml
import matplotlib.image as mpimg
import numpy as np
from astropy.io import fits

# import matplotlib.pyplot as plt
# import astropy.units as u
# import glob
import pandas as pd
import seaborn as sns
import os

sns.set(style="ticks", context="talk")

# import config.yaml file

with open("/Users/mmckay/phd_projects/breakBRD/conf/main.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def reduce_IFU_table(df):
    """
    Reduce the IFU table to remove outliers from the table (i.e. Ha/Hb < 2.86) before making the supercsv file

    """
    # df = df.drop_duplicates(inplace=True)
    # Halpha/Hbeta reduction
    df = df[df["HA/HB"] > 2.86]

    # Remove Age_LW < 5.0
    df = df[df["GYR_LW"] > 5.0]

    # Remove spaxels with Halpha SNR < 5
    df = df[df["HALPHA SNR"] > 5.0]

    return df


def make_super_csv(global_db_df, csv_files_dir, super_csv_fn):
    # Combine all dataframes into a super dataframe
    super_csv_df = []
    for plateifu in global_db_df["plateifu"]:
        # Read in MAP csv file
        df = pd.read_csv("{}{}_map.csv".format(csv_files_dir, plateifu))
        # Drop Unnamed column # TODO set index
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        df.drop_duplicates(inplace=True)
        # Add column for plateifu tracking
        df["plateifu"] = plateifu

        # Reduce the the table and replace the old table
        df = reduce_IFU_table(df)
        df.to_csv("{}{}_map.csv".format(csv_files_dir, plateifu))

        # Append table to super_csv_df
        super_csv_df.append(df)

    # Combine csv files
    super_csv = pd.concat(super_csv_df)
    super_csv.drop_duplicates(inplace=True)
    # Replace inf value with nans
    super_csv_noinfs = super_csv.replace([np.inf, -np.inf], np.nan)

    # Make supercsv
    super_csv_noinfs.to_csv(
        "{}{}.csv".format(config["data"]["supercsv_dir"], super_csv_fn)
    )

    return super_csv_noinfs


# Seperate the lg12 table into SF/GV/QC galaxies
def seperate_lg12_table_into_sf_gv_qc(lg12_global_df):
    # Seperate the lg12 table into SF/GV/QC galaxies
    sf_lg12_global_df = lg12_global_df[(
        lg12_global_df["Dn4000SDSSindx "] < 1.5)]
    gv_lg12_global_df = lg12_global_df[
        lg12_global_df["Dn4000SDSSindx "].between(1.5, 1.75)
    ]
    qc_lg12_global_df = lg12_global_df[(
        lg12_global_df["Dn4000SDSSindx "] > 1.75)]

    return sf_lg12_global_df, gv_lg12_global_df, qc_lg12_global_df


if __name__ == "__main__":
    # Read in the lg12 and bbrd global tables
    lg12_global_df = pd.read_csv(config["data"]["lg12_global_table"])
    bbrd_global_df = pd.read_csv(config["data"]["bbrd_global_table"])
    print("BBRD # {}".format(len(bbrd_global_df)))

    # Remove AGN and Merger galaxy from the BBRD global table:
    bbrd_global_df = bbrd_global_df[
        ~bbrd_global_df["plateifu"].isin(
            ["9183-3703", "11827-1902", "8595-3703"])
    ]
    print("BBRD # {}".format(len(bbrd_global_df)))
    bbrd_global_df.to_csv(config["data"]["11_bbrd_global_table"])

    # Make BBRD supercsv
    bbrd_lg12_supercsv_df = make_super_csv(
        bbrd_global_df, config["data"]["all_csv_dir"], "bbrd_superifu"
    )
    #!---------------------------------------------------------------------------------------------------------------------
    #! Seperate the lg12 table into SF/GV/QC galaxies
    (
        sf_lg12_global_df,
        gv_lg12_global_df,
        qc_lg12_global_df,
    ) = seperate_lg12_table_into_sf_gv_qc(lg12_global_df)

    print("CSF # {}".format(len(sf_lg12_global_df)))
    print("CGV # {}".format(len(gv_lg12_global_df)))
    print("CQC # {}\n".format(len(qc_lg12_global_df)))

    #! Limit mass range of CSF CGV CQC galaxies
    min_mass = bbrd_global_df["Mstarmed_SDSStotlgm"].describe()["min"]
    max_mass = bbrd_global_df["Mstarmed_SDSStotlgm"].describe()["max"]

    # Limit mass range of LG12 CSF and CQC sample
    sf_lg12_global_df = sf_lg12_global_df[
        sf_lg12_global_df["Mstarmed_SDSStotlgm"].between(min_mass, max_mass)
    ]

    qc_lg12_global_df = qc_lg12_global_df[
        qc_lg12_global_df["Mstarmed_SDSStotlgm"].between(min_mass, max_mass)
    ]

    gv_lg12_global_df = gv_lg12_global_df[
        gv_lg12_global_df["Mstarmed_SDSStotlgm"].between(min_mass, max_mass)
    ]

    # Save vetted global data as CSV
    sf_lg12_global_df.to_csv(config["data"]["csf_global_table"])
    qc_lg12_global_df.to_csv(config["data"]["cqc_global_table"])
    gv_lg12_global_df.to_csv(config["data"]["cgv_global_table"])

    print("CSF # {}".format(len(sf_lg12_global_df)))
    print("CGV # {}".format(len(gv_lg12_global_df)))
    print("CQC # {}".format(len(qc_lg12_global_df)))
    #!----------------------------------------------------------------------------------------------------------------------------

    # Remove visually rejected galaxies from the global tables
    if os.path.exists(config["rejects"]["vis_rejects_global_table"]):
        print("Reject table exists - removing rejected galaxies from global tables")
        vis_rejects_global_df = pd.read_csv(
            config["rejects"]["vis_rejects_global_table"]
        )
        sf_lg12_global_df = sf_lg12_global_df[
            ~sf_lg12_global_df["plateifu"].isin(
                vis_rejects_global_df["plateifu"])
        ]
        qc_lg12_global_df = qc_lg12_global_df[
            ~qc_lg12_global_df["plateifu"].isin(
                vis_rejects_global_df["plateifu"])
        ]
        gv_lg12_global_df = gv_lg12_global_df[
            ~gv_lg12_global_df["plateifu"].isin(
                vis_rejects_global_df["plateifu"])
        ]
        #! Make supercsv of for cut files
        # TODO: add supercsv for the lg12 and bbrd tables
        sf_lg12_supercsv_df = make_super_csv(
            sf_lg12_global_df, config["data"]["all_csv_dir"], "csf_superifu"
        )
        gv_lg12_supercsv_df = make_super_csv(
            gv_lg12_global_df, config["data"]["all_csv_dir"], "cgv_superifu"
        )
        qc_lg12_supercsv_df = make_super_csv(
            qc_lg12_global_df, config["data"]["all_csv_dir"], "cqc_superifu"
        )

    else:
        print(
            "Reject table does not exist - continuing without removing rejected galaxies from global tables"
        )
        # Make supercsv files to calculate the frequncy weighted median and the distrubution
        #! Make supercsv of for cut files
        # TODO: add supercsv for the lg12 and bbrd tables
        sf_lg12_supercsv_df = make_super_csv(
            sf_lg12_global_df, config["data"]["all_csv_dir"], "csf_superifu"
        )
        gv_lg12_supercsv_df = make_super_csv(
            gv_lg12_global_df, config["data"]["all_csv_dir"], "cgv_superifu"
        )
        qc_lg12_supercsv_df = make_super_csv(
            qc_lg12_global_df, config["data"]["all_csv_dir"], "cqc_superifu"
        )
