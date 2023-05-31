"""
Creates separate YAMP job scripts for each sample.
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
input_dir = project_dir.joinpath("data")

# Ignore this line if the input directory does not contain subdirectories
input_subdirs = [Path("Comte/lane6"), Path("Comte/lane7"), Path("Comte/lane8"), Path("Edge/lane6"), Path("Edge/lane7"),
                 Path("Edge/lane8")]

output_dir = project_dir.joinpath("QC")
stdout_dir = output_dir.joinpath("yamp_stdout")
stderr_dir = output_dir.joinpath("yamp_stderr")
output_dir.mkdir(parents=True, exist_ok=True)
stdout_dir.mkdir(parents=True, exist_ok=True)
stderr_dir.mkdir(parents=True, exist_ok=True)

for indir in input_subdirs:
    current_dir = input_dir.joinpath(indir)
    forward_files = glob.glob(f"{current_dir}/*_R1.fq.gz")
    outdir = output_dir.joinpath(indir)
    outdir.mkdir(parents=True, exist_ok=True)

    for file in forward_files:
        sample_name = Path(file).name.split("_R1.fq.gz")[0]
        job_name = f"{sample_name}_QC"
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
        module_load = (f"module load StdEnv/2020 python/3.11.2 nextflow/22.10.6 java/17.0.2 fastqc/0.11.9 bbmap/38.86 "
                       f"bowtie2/2.4.4 gcc/11.3.0 samtools/1.17 diamond/2.1.6\n"
                       f"source {install_dir}/YAMP_env/bin/activate\n\n")
        organize_slurm = (f"cd $SLURM_TMPDIR\n"
                          f"cp {current_dir}/{sample_name}_R1.fq.gz ./\n"
                          f"cp {current_dir}/{sample_name}_R2.fq.gz ./\n\n")
        yamp_command = (f"nextflow run {install_dir}/YAMP/YAMP.nf --reads1 {sample_name}_R1.fq.gz "
                        f"--reads2 {sample_name}_R2.fq.gz --prefix {sample_name} --outdir {outdir} --mode QC "
                        f"--dedup true -profile base\n")

        with open(f"./{job_name}.sh", "w") as f_output:
            f_output.write(header)
            f_output.write(module_load)
            f_output.write(organize_slurm)
            f_output.write(yamp_command)
