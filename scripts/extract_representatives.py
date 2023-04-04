"""
1st argument: .clstr file (cdhit output);
2nd argument: .faa file (cdhit input);

output: throws to stdout the .faa file containing only cluster representatives
"""
import sys


def clstr_rep_fasta(clstr_file, fasta_file):
    """
    Write all the clstr representatives to a fasta file in stdout.
    """
    sequence_info = {}
    with open(fasta_file, "r", encoding="UTF-8") as fasta_input:
        for line in fasta_input:
            if line.startswith(">"):
                current_name = line.strip().split()[0]
                sequence_info[current_name] = [line.strip(), ""]
            else:
                sequence_info[current_name][1] += line.strip()

    with open(clstr_file, "r", encoding="UTF-8") as clstr_input:
        for line in clstr_input:
            if line.startswith(">Cluster"):
                current_cluster = line.strip()
            elif line.strip().endswith(r"*"):
                seq = sequence_info[line.split()[2].rstrip(r"...")][1]
                print(f"{current_cluster}\n{seq}")

if __name__ == "__main__":

    clstr_rep_fasta(sys.argv[1], sys.argv[2])
