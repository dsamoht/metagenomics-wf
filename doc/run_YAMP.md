# Quality control with [YAMP](https://github.com/alesssia/YAMP)

## __1. Installation__

### 1.0 Move to your $INSTALL_PATH
```
cd $INSTALL_PATH
```
### 1.1 Create a Python environnement for YAMP and its dependencies
```
module load python/3.8.10 nextflow/21.04.3 java/14.0.2 fastqc/0.11.9 bbmap/38.86 bowtie2/2.4.4 gcc/9.3.0 samtools/1.13 diamond/2.0.13

python -m venv YAMP_env
source YAMP_env/bin/activate
```
### 1.2 Install and test BBMAP
```
# Install BBMAP
mkdir BBMap && cd BBMap
wget https://sourceforge.net/projects/bbmap/files/BBMap_38.98.tar.gz ./
tar -xvzf BBMap_38.98.tar.gz

# Test BBMAP
bbmap/stats.sh in=bbmap/resources/phix174_ill.ref.fa.gz 
cd ..
```
### 1.3 Update pip installer and install Biobakery 3+
```
pip install --no-index --upgrade pip
pip install humann
humann_test --run-functional-tests-tools
```
### 1.4 Install Multiqc
```
pip install multiqc
```
### 1.5 Install Metaphlan
```
pip install metaphlan
```
### 1.4 Install YAMP
```
# clone the github repository
git clone https://github.com/alesssia/YAMP.git
cd YAMP

# Download the database of contaminants
cd ./assets/data/
wget https://zenodo.org/record/4629921/files/hg19_main_mask_ribo_animal_allplant_allfungus.fa.gz

# create directories for the annotation databases so that YAMP does not throw errors, specifically chocophlan, metaphlan_databases and uniref
# we limit YAMP only to the QC steps; we can leave them empty

mkdir chocophlan
mkdir metaphlan_databases
mkdir uniref
```

## __2. Run YAMP (slurm job script example)__
```
#!/bin/bash
#SBATCH --job-name=sampleA_YAMP
#SBATCH --output=${STUDY_PATH}/raw_reads/YAMP_stdout/sampleA_YAMP.stdout
#SBATCH --error=${STUDY_PATH}/raw_reads/YAMP_stderr/sampleA_YAMP.stderr
#SBATCH --account=rrg-yourpi
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=20
#SBATCH --mem=80G

module load module load StdEnv/2020 python/3.11.2 nextflow/22.10.6 java/17.0.2 fastqc/0.11.9 bbmap/38.86 bowtie2/2.4.4 gcc/11.3.0 samtools/1.17 diamond/2.1.6

source $INSTALL_PATH/env_YAMP/bin/activate

cd $SLURM_TMPDIR
cp ${STUDY_PATH}/raw_reads/sampleA_R1_001.fastq.gz ./
cp ${STUDY_PATH}/raw_reads/sampleA_R2_001.fastq.gz ./


nextflow run $INSTALL_PATH/YAMP/YAMP.nf --reads1 sampleA_R1_001.fastq.gz --reads2 sampleA_R2_001.fastq.gz --prefix sampleA --outdir ${STUDY_PATH}/QCd_reads/sampleA_QCd/ --mode QC --dedup true -profile base
```

#### __acknowledgment__: instructions adapted from a script by Sasha-William Ménard-Mérette
[Global workflow](../README.md)