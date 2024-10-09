# Cluster filtering and selection

# 1. Filter clusters according to databases

## 1.1 Create python environment and install required modules

```
python -m venv $INSTALL_PATH/cog_env
source $INSTALL_PATH/bin/activate

pip install numpy
pip install pandas
```

## 1.2 Run filtration script #1

```
python filter_gene_clusters.py ${STUDY_PATH}/QCd_reads/study_all_clusters_c70.tsv
```
The script will save on disk .pickle files corresponding to matrices of clusters matching the different databases (ex: "CAZy_clstr.pkl") as well as the file corresponding to all clusters (no database filtering).


# 2. Divide the [COG](https://www.ncbi.nlm.nih.gov/research/cog#) database into 25 sub-categories

## 2.1 Download the COG database metadata

```
wget https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/cog-20.cog.csv
wget https://ftp.ncbi.nih.gov/pub/COG/COG2020/data/cog-20.def.tab
```

## 2.2 Clean up the COG metadata
As of 2023-06-16, cog-20.cog.csv contains superfluous commas at multiple lines, which breaks the filtration script.
Use a combination of `awk`, `grep` and `sed` to find the relevant lines and remove the problematic commas.
```
# Make a backup just in case
cp cog-20.cog.csv cog-20.cog.csv.backup

# These are the lines that contain the wrong number of fields
lines=`awk -F ',' '{ print NF != 13 }' cog-20.cog.csv | grep -n 1 | sed 's/:1$//g'`

for l in ${lines[@]}
do
  sed -i "${l}s/,$//" cog-20.cog.csv
done
```

## 2.3 Run filtration script #2

```
python split_cog_db.py ${STUDY_PATH}/QCd_reads/study_all_clusters_c70.clstr ${STUDY_PATH}/QCd_reads/ALL_clstr.pkl
```
Will produce COG_{A,B,...,X,Z}_clstr.pkl files.


# 3. Filter clusters according to specific protein domains

## 3.1 Extract representative sequences from all clusters

We select clusters whose representatives contain specific protein domains.

```
python extract_representatives.py ${STUDY_PATH}/QCd_reads/study_all_clusters_c70.clstr ${STUDY_PATH}/QCd_reads/study_all.faa > ${STUDY_PATH}/QCd_reads/study_all_clusters_c70_representatives.faa
```

## 3.2 Search protein domains in representatives sequences (slurm job script example)

```
#!/bin/bash
#SBATCH --job-name=hmmer_search_study
#SBATCH --output=hmmer_search_study.stdout
#SBATCH --error=hmmer_search_study.stderr
#SBATCH --account=rrg-fraymond
#SBATCH --nodes=1
#SBATCH --time=4:00:00
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=4000M

module load nixpkgs/16.09  gcc/7.3.0 hmmer/3.1b2

# search domains with hmmer
hmmsearch --tblout study_all_clusters_GBA_domains.hmmout.tsv --cpu 32 -E 0.001 pfam_domains.hmm ${STUDY_PATH}/QCd_reads/study_all_clusters_c70_representatives.faa

# parse hmmer's output - output clusters that had hits

grep ">Cluster_" study_all_clusters_GBA_domains.hmmout.tsv | awk '{print $1}' | sed "s/>//g" > study_all_GBA_clusters.txt

python filter_gene_clusters_from_list.py ${STUDY_PATH}/QCd_reads/study_all_clusters_c70.clstr ${STUDY_PATH}/QCd_reads/ALL_clstr.pkl study_all_GBA_clusters.txt
```

[Global workflow](../README.md#global-workflow)
