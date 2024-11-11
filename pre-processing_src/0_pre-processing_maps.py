"""
Description:
Pre-processing lg12 and bbrd sample

1. replace inf values with nan
2. drop duplicates
3. Remove bbrd galaxies from lg12 tables
"""
import numpy as np
import pandas as pd
import yaml  # import config.yaml file

with open("/Users/mmckay/phd_projects/breakBRD_radial_profiles_analysis/conf/main.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def replace_inf_with_nan(df):
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    return df


def drop_duplicates(df):
    df.drop_duplicates(subset="plateifu", inplace=True)
    return df


def remove_bbrd_galaxies_from_lg12_tables(lg12_df, bbrd_df):
    # Remove bbrd galaxies from lg12 tables
    lg12_df = lg12_df[~lg12_df["plateifu"].isin(bbrd_df["plateifu"])]
    return lg12_df


if __name__ == "__main__":
    # Read in the lg12 and bbrd global tables
    bbrd_global_df = pd.read_csv(config["data"]["bbrd_global_table"])
    lg12_global_df = pd.read_csv(config["data"]["lg12_global_table"])

    # Pre-process bbrd global tables
    bbrd_global_df = replace_inf_with_nan(bbrd_global_df)
    bbrd_global_df = drop_duplicates(bbrd_global_df)
    bbrd_global_df.to_csv(config["data"]["bbrd_global_table"], index=False)

    # Pre-process lg12 global tables
    lg12_global_df = replace_inf_with_nan(lg12_global_df)
    lg12_global_df = drop_duplicates(lg12_global_df)
    lg12_global_df = remove_bbrd_galaxies_from_lg12_tables(
        lg12_global_df, bbrd_global_df
    )
    lg12_global_df.to_csv(config["data"]["lg12_global_table"], index=False)
    # print(len(lg12_global_df))
    lg12_global_df.to_csv(config["data"]["lg12_global_table"])
