# Clusters of orthologous groups of proteins (COGs) with [cdhit](https://github.com/weizhongli/cdhit)

## __1. Prepare input files__

## 1.1 Edit sample files
To retrieve from which sample the sequences are from after the clustering, we modify the headers in the protein files so that they contain the sample id.

Example (save a .backup file if you're not sure of your command):
```
sed -i.backup "s/^>/>sampleA|/g" ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_prodigal_output/sampleA.faa
```
To be done for all protein files prior to the next step.

## 1.2 Combine all protein files from samples and from databases
```
for file in $(find ${STUDY_PATH}/QCd_reads/ | grep prodigal_output | grep .faa$)
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
cd-hit -i ${STUDY_PATH}/QCd_reads/study_all.faa -o ${STUDY_PATH}/QCd_reads/study_all_clusters_c70 -c 0.70 -d 0 -M 0 -T 0 -g 1 -G 1

# transform cdhit output in tabular format
python matrix_from_cdhit.py ${STUDY_PATH}/QCd_reads/study_all_clusters_c70.clstr > ${STUDY_PATH}/QCd_reads/study_all_clusters_c70.tsv
```

[Global workflow](../README.md#global-workflow)
