"""
argument: cdhit output in tabular format

output: .pickle files corresponding to the clusters of each databases
        + 1 .pickle file corresponding to all clusters
"""
import sys
import pickle

import numpy as np
import pandas as pd



db_names = [
      "BGC",
      "BRENDA",
      "CAZy",
      "COG",
      "MERGEM_IS",
      "MERGEM_RG"
     ]

clstr = pd.read_csv(sys.argv[1], sep="\t", header=0, index_col=0)

clstr_dbs = clstr[db_names]
clstr.drop(labels=db_names, axis=1, inplace=True)
ratio = clstr.div(clstr.sum(axis=0), axis=1)
ratio[db_names] = clstr_dbs

def common_features(dataframe):
    """
    Keep variables shared by at least 2 samples
    """
    data_bin = pd.DataFrame(np.where(dataframe>0, 1, 0),
                            index=list(dataframe.index.values),
                            columns=list(dataframe.columns.values))
    mat_bled = data_bin.loc[:, data_bin.sum() >= 2]
    return dataframe.loc[:, mat_bled.columns.values]

for db in db_names:

    db_filtered = ratio[ratio[db] > 0]
    db_filtered = db_filtered.drop(labels=db_names, axis=1)
    db_filtered = common_features(db_filtered.transpose())
    with open(f"{db}_clstr.pkl", "wb") as db_filtered_output:
        pickle.dump(db_filtered, db_filtered_output)

all_clstr = ratio.drop(labels=db_names, axis=1)
all_clstr = common_features(all_clstr.transpose())
with open("ALL_clstr.pkl", "wb") as all_clstr_output:
    pickle.dump(all_clstr, db_filtered_output)
