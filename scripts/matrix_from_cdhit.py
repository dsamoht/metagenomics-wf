"""
Adapted from a script by Pier-Luc Plante

argument: .clstr file (cdhit output)

output: throws to stdout the resulting matrix
"""
import sys


if __name__ == "__main__":

    current_cluster = ""
    cluster_dict = {}
    samples_name = []

    with open(sys.argv[1], encoding="UTF-8") as clstr_input:
        for line in clstr_input:
            if line == "":
                break
            if line[0] == '>':
                entry_name = line.split()[0].split('>')[1]+'_'+line.split()[1]
                cluster_dict[entry_name] = []
                current_cluster = entry_name
            else:
                sample_id = (line.split()[2].split('|')[0])[1:]
                cluster_dict[entry_name].append(sample_id)
                if sample_id not in samples_name:
                    samples_name.append(sample_id)


    #to throw the info in a .tsv format to stdout
    line = "ClusterID"
    samples_name.sort()
    for name in samples_name:
        line = line+'\t'+name
    print(line)

    for entry, val in cluster_dict.items():
        line_start = str(entry)
        line_content = ""
        line_total = 0
        for name in samples_name:
            if name in val:
                line_content = line_content +'\t' + str(val.count(name))
                line_total += 1
            else:
                line_content += '\t0'
        line = line_start + line_content
        print(line)
