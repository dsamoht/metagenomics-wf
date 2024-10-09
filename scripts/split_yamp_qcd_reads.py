"""
1st argument: Path to directory containing QC'd reads from both R1 and R2 (YAMP output)

output : 2 files : '[...]_R1.fastq.gz' and '[...]_R2.fastq.gz' containing
             forward and reverse reads, respectively. Sequences with no reverse
             or forward mate are discarded.
"""
import sys
import gzip
import re
from pathlib import Path
from itertools import zip_longest


def parse_zip_longest(input_fastq):
    """
    Iterator to speed up fastq parsing.
    source : https://groverj3.github.io/
    """
    with gzip.open(input_fastq, 'rt') as input_handle:
        fastq_iterator = (line.rstrip() for line in input_handle)
        for entry in zip_longest(*[fastq_iterator] * 4):
            yield entry


if __name__ == "__main__":

    r1_id_to_seq = {}
    r2_id_to_seq = {}

    # I/O file names
    file_ = Path(sys.argv[1])
    file_name = file_.name
    sample_name = file_name.replace("_QCd.fq.gz", "")
    output_name_r1 = file_.parent.joinpath(sample_name + "_QCd_R1.fq.gz")
    output_name_r2 = file_.parent.joinpath(sample_name + "_QCd_R2.fq.gz")

    # Change this to the forward and reverse identifiers
    fwd_identifier, rv_identifier = "1:N:0", "2:N:0"
    baseID_r1, baseID_r2 = {}, {}

    for record in parse_zip_longest(file_):
        if re.search(fwd_identifier, record[0]):
            r1_id_to_seq[record[0]] = record[1], record[2], record[3]
            baseID_r1[record[0].split()[0]] = record[0]
        elif re.search(rv_identifier, record[0]):
            r2_id_to_seq[record[0]] = record[1], record[2], record[3]
            baseID_r2[record[0].split()[0]] = record[0]

    # 2. Remove reads w/o both forward and reverse
    common_ids = set(baseID_r1.keys()).intersection(set(baseID_r2.keys()))

    # 3. Save forward and reverse reads in two files
    with gzip.open(output_name_r1, "wt") as output_forward, gzip.open(output_name_r2, "wt") as output_reverse:
        for common_id in list(common_ids):
            id_r1 = baseID_r1[common_id]
            seq_r1 = r1_id_to_seq[id_r1]
            output_forward.write(id_r1 + "\n")
            output_forward.write(seq_r1[0] + "\n")
            output_forward.write(seq_r1[1] + "\n")
            output_forward.write(seq_r1[2] + "\n")

            id_r2 = baseID_r2[common_id]
            seq_r2 = r2_id_to_seq[id_r2]
            output_reverse.write(id_r2 + "\n")
            output_reverse.write(seq_r2[0] + "\n")
            output_reverse.write(seq_r2[1] + "\n")
            output_reverse.write(seq_r2[2] + "\n")
