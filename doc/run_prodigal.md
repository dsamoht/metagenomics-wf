# Gene prediction and translation with [Prodigal](https://github.com/hyattpd/Prodigal)


## __Run Prodigal (slurm job script example)__

```
#!/bin/bash
#SBATCH --job-name=sampleA_assembly_to_protein
#SBATCH --output=${STUDY_PATH}/QCd_reads/prodigal_stdout/sampleA_assembly_to_protein.stdout
#SBATCH --error=${STUDY_PATH}/QCd_reads/prodigal_stderr/sampleA_assembly_to_protein.stderr
#SBATCH --account=rrg-yourpi
#SBATCH --time=8:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=9

module load StdEnv/2020 prodigal/2.6.3

prodigal -i ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_megahit_output/final.contigs.fa -o ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_prodigal_output/sampleA.coords.gbk -a ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_prodigal_output/sampleA.faa -p meta
```
[Global workflow](../README.md#global-workflow)
