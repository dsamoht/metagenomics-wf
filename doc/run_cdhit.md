# Clusters of orthologous groups of proteins (COGs) with [cdhit](https://github.com/weizhongli/cdhit)

## __1. Prepare input files__

## 1.1 Edit sample files
To retrieve from which sample the sequences are from after the clustering, we modify the headers of contigs in the assembly files so that they contain the sample's id.

Example:
```
sed -i.backup "s/^>/>$sampleA|/g" ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_megahit_output/final.contigs.fa
```
## 1.2 Combine all sample files and databases
```
for file in $(find ${STUDY_PATH}/QCd_reads/ | grep final.contigs.fa)
do
    cat $file >> ${STUDY_PATH}/QCd_reads/study_all.faa
done

# add protein databases
cat BRENDA_CAZy_COG_MERGEM_MIBiG_2022-09.pep >> ${STUDY_PATH}/QCd_reads/study_all.faa
```

## __2. Run cdhit (slurm job script example)__

```
#!/bin/bash
#SBATCH --job-name=cdhit_job
#SBATCH --output=cdhit_job.stdout
#SBATCH --error=cdhit_job.stderr
#SBATCH --account=rrg-fraymond
#SBATCH --time=48:00:00
#SBATCH --mem=125G
#SBATCH --cpus-per-task=32

module load StdEnv/2020 cd-hit/4.8.1
cd-hit -i ${STUDY_PATH}/QCd_reads/study_all.faa -o cdhit_data/CMI2_n510_c70 -c 0.70 -d 0 -M 0 -T 0 -g 1 -G 1

module load StdEnv/2020 megahit/1.2.9
megahit -1 ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_QCd_R1.fq.gz -2 ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_QCd_R2.fq.gz -t 9 -o ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_megahit_output
```

[Global workflow](../README.md)