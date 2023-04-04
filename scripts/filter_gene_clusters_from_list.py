"""
1st argument: .pickle file corresponding to all gene clusters
2nd argument: file containing the list of clusters to keep (1 cluster per line)
                Cluster_1
                Cluster_2
                Cluster_4
                ...
                Cluster_345

output: .pickle cluster matrix file with only clusters present in the given list.
"""
import pickle
import sys

NAME = "GBA"


if __name__ == "__main__":

    clstr_df_file = sys.argv[1]
    clstr_list_file = sys.argv[2]
    clstr_list = []

    with open(clstr_list_file, "r", encoding="UTF-8") as clstr_list_input:
        for line in clstr_list_input:
            clstr_list.append(line.strip())

    with open(clstr_df_file, "rb") as clstr_df_input:
        clstr_df = pickle.load(clstr_df_input)
    clusters_ = list(set(clstr_df.columns).intersection(set(clstr_list)))

    with open(f"{NAME}_clstr.pkl", "rb") as filtered_clstr_df_output:
        pickle.dump(clstr_df[clusters_], filtered_clstr_df_output)
