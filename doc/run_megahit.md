# Assembly with [megahit](https://github.com/voutcn/megahit)

## __1. Prepare input files__
When given paired-end reads, megahit requires that the forward and reverse files contain only matching sequences (i.e sequences with both forward and reverse). Because YAMP yields different number of forward and reverse reads, we have to modify the output by keeping only matching reads.

Ex:
```
python split_yamp_qcd_reads.py ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_QCd.fq.gz
```
It produces 2 files: sampleA_QCd_R1.fq.gz and sampleA_QCd_R2.fq.gz


## __2. Run megahit (slurm job script example)__

```
#!/bin/bash
#SBATCH --job-name=sampleA_QC_reads_to_assembly
#SBATCH --output=${STUDY_PATH}/QCd_reads/megahit_stdout/sampleA_QC_reads_to_assembly.stdout
#SBATCH --error=${STUDY_PATH}/QCd_reads/megahit_stderr/sampleA_QC_reads_to_assembly.stderr
#SBATCH --account=rrg-yourpi
#SBATCH --time=8:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=9

module load StdEnv/2020 megahit/1.2.9
megahit -1 ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_QCd_R1.fq.gz -2 ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_QCd_R2.fq.gz -t 9 -o ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_megahit_output
```
[Global workflow](../README.md#global-workflow)
