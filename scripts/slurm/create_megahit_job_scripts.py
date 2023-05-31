"""
Creates separate megahit job scripts for each sample.
1st argument: Project directory (${STUDY_PATH})
"""
import glob
import sys
from pathlib import Path

# Change slurm flags as desired
account = "def-jcomte"
time = "1:00:00"
cpus = "32"
memory = "4G"

project_dir = Path(sys.argv[1])
install_dir = project_dir.joinpath("install")
input_dir = project_dir.joinpath("QC")

# Ignore this line if the input directory does not contain subdirectories
input_subdirs = [Path("Comte/lane6"), Path("Comte/lane7"), Path("Comte/lane8"), Path("Edge/lane6"), Path("Edge/lane7"),
                 Path("Edge/lane8")]

stdout_dir = project_dir.joinpath("megahit_stdout")
stderr_dir = project_dir.joinpath("megahit_stderr")
stdout_dir.mkdir(parents=True, exist_ok=True)
stderr_dir.mkdir(parents=True, exist_ok=True)

for indir in input_subdirs:
    current_dir = input_dir.joinpath(indir)
    qcd_samples = glob.glob(f"{current_dir}/*")

    for sample_dir in qcd_samples:
        sample_name = Path(sample_dir).name
        job_name = f"{sample_dir}_QC_reads_to_assembly"
        sbatch_out = stdout_dir.joinpath(f"{job_name}.stdout")
        sbatch_err = stderr_dir.joinpath(f"{job_name}.stderr")

        header = (f"#!/bin/bash\n"
                  f"#SBATCH --job-name={job_name}\n"
                  f"#SBATCH --output={sbatch_out}\n"
                  f"#SBATCH --error={sbatch_err}\n"
                  f"#SBATCH --account={account}\n"
                  f"#SBATCH --time={time}\n"
                  f"#SBATCH --cpus-per-task={cpus}\n"
                  f"#SBATCH --mem-per-cpu={memory}\n\n")
        run_megahit = (f"module load StdEnv/2020 megahit/1.2.9\n"
                       f"megahit -1 {sample_dir}/{sample_name}_QCd_R1.fq.gz -2 {sample_dir}/{sample_name}_QCd_R2.fq.gz "
                       f"-t 9 -o {sample_dir}/{sample_name}_megahit_output\n")

        with open(f"./{job_name}.sh", "w") as f_output:
            f_output.write(header)
            f_output.write(run_megahit)
