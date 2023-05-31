"""
1st argument: Path to directory containing QC'd reads from both R1 and R2 (YAMP output)

output : 2 files : '[...]_R1.fastq.gz' and '[...]_R2.fastq.gz' containing
             forward and reverse reads, respectively. Sequences with no reverse
             or forward mate are discarded.
"""
import sys
import gzip
import glob
from pathlib import Path
from itertools import zip_longest


def parse_zip_longest(input_fastq):
    """
    Iterator to speed up fastq parsing.
    source : https://groverj3.github.io/
    """
    with gzip.open(input_fastq, 'rt') as input_handle:
        fastq_iterator = (line.rstrip() for line in input_handle)
        for record in zip_longest(*[fastq_iterator] * 4):
            yield record


def find_identifier(input_fastq):
    """
    Find the "direction" identifier (ex ":1" and ":2") for forward and
    reverse reads.
    """
    fwd_identifier, rv_identifier = "", ""
    headers = []
    for record in parse_zip_longest(input_fastq):
        headers.append(record[0])
    first, second = sorted(headers)[0:2]
    if len(first) != len(second):
        raise ValueError(f"Identifier not found in sequences {first} and {second}.")

    for _, char in enumerate(first):
        if char != second[_]:
            fwd_identifier += char
            rv_identifier += second[_]
            pos = _

    return fwd_identifier, rv_identifier, pos


if __name__ == "__main__":

    # Add your input subdirectories here
    input_subdirs = [Path("Comte/lane6"), Path("Comte/lane7"), Path("Comte/lane8"), Path("Edge/lane6"),
                     Path("Edge/lane7"), Path("Edge/lane8")]

    for indir in input_subdirs:
        current_dir = Path(sys.argv[1]).joinpath(indir)
        qcd_samples = glob.glob(f"{current_dir}/*")
        for sample in qcd_samples:
            r1_id_to_seq = {}
            r2_id_to_seq = {}

            # I/O file names
            sample_name = Path(sample).name
            file_ = Path(sample).joinpath(sample_name + "_QCd.fq.gz")
            output_name_r1 = Path(sample).joinpath(sample_name + "_QCd_R1.fq.gz")
            output_name_r2 = Path(sample).joinpath(sample_name + "_QCd_R2.fq.gz")

            fwd_identifier, rv_identifier, pos = find_identifier(file_)
            baseID_r1, baseID_r2 = {}, {}

            for record in parse_zip_longest(file_):
                if record[0][pos] == fwd_identifier:
                    r1_id_to_seq[record[0]] = record[1], record[2], record[3]
                    baseID_r1[record[0].split()[0]] = record[0]
                elif record[0][pos] == rv_identifier:
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
