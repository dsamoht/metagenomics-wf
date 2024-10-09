"""
1st argument: cdhit output (.clstr file)
2nd argument: .pickle file corresponding to all gene clusters

output: COG_`categorie`_clstr.pkl files
"""


import pickle
import re
import sys

import pandas as pd


gene_to_cog_number = pd.read_csv("cog-20.cog.csv", index_col=None, header=None)
cog_number_to_cat = pd.read_csv("cog-20.def.tab", sep="\t", index_col=None, header=None, encoding="cp1252")

cog_number_to_category_dict = dict(zip(cog_number_to_cat[0], cog_number_to_cat[1]))
gene_to_cog_number_dict = {}


for i in range(gene_to_cog_number.shape[0]):
    gene = gene_to_cog_number.iloc[i, 2]
    cog_number = gene_to_cog_number.iloc[i, 6]
    cog_category = cog_number_to_category_dict[cog_number]
    if gene in gene_to_cog_number_dict:
        if cog_number not in gene_to_cog_number_dict[gene]:
            gene_to_cog_number_dict[gene] += list(cog_category)
    else:
        gene_to_cog_number_dict[gene] = list(cog_category)

for gene, list_ in gene_to_cog_number_dict.items():
    tmp = list(set(list_))
    gene_to_cog_number_dict[gene] = tmp


clstr_to_cog_category = {}
with open(sys.argv[1], "r", encoding="UTF-8") as clstr_input:
    for line in clstr_input:
        if line.startswith(">Cluster"):
            currentCluster = "Cluster_" + line.split()[1]
        elif re.search(">COG", line):
            gene = line.split("COG|")[1].split("...")[0]
            try:
                for cat in gene_to_cog_number_dict[gene]:
                    if cat not in clstr_to_cog_category:
                        clstr_to_cog_category[cat] = [currentCluster]
                    else:
                        clstr_to_cog_category[cat].append(currentCluster)
            except KeyError:
                last_underscore_i = gene.rfind("_")
                tmp = gene[:last_underscore_i] + "." + gene[last_underscore_i+1:]
                for cat in gene_to_cog_number_dict[tmp]:
                    if cat not in clstr_to_cog_category:
                        clstr_to_cog_category[cat] = [currentCluster]
                    else:
                        clstr_to_cog_category[cat].append(currentCluster)

with open(sys.argv[2], "rb") as pickled_df:
    base_df = pickle.load(pickled_df)
clstr_base = set(base_df.columns.values)

for cat, clusters in clstr_to_cog_category.items():
    common_clstr = list(clstr_base.intersection(set(clusters)))
    df_output = base_df[common_clstr]
    with open(f"COG_{cat}_clstr.pkl", "wb") as pickled_output:
        pickle.dump(df_output, pickled_output)
