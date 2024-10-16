# Using [MetaPhlAn](https://github.com/biobakery/MetaPhlAn/wiki/MetaPhlAn-4) and [HUMAnN](https://huttenhower.sph.harvard.edu/humann/) for taxonomic and functional profiles

> __*Note*__: we execute *MetaPhlAn4* prior to *HUMAnN3* (the latest release of both softwares). It prevents to tumble on dependencies problems.

## __1. Create a python environnement for MetaPhlAn and its dependencies__
INSTALL_PATH: a directory for the environnement and the databases
```
module load StdEnv/2020 python/3.11.2 bowtie2/2.4.4
python -m venv $INSTALL_PATH/metaphlan_env
source $INSTALL_PATH/metaphlan_env/bin/activate
```
## __2. Install MetaPhlAn and the required databases__

```
pip install MetaPhlAn
```
Download the *MetaPhlAn* database
```
metaphlan --install
```
## __3. Create a python environnement for HUMAnN and its dependencies__
INSTALL_PATH: a directory for the environnement and the databases
```
module load StdEnv/2020 python/3.11.2
python -m venv $INSTALL_PATH/humann_env
source $INSTALL_PATH/humann_env/bin/activate
```
## __4. Install HUMAnN and the required databases__

```
pip install humann --no-binary :all:
```
Download the *UniRef* database
```
humann_databases --download uniref uniref90_diamond $INSTALL_PATH --update-config yes
```
Download the *ChocoPhlAn* database
```
humann_databases --download chocophlan full $INSTALL_PATH --update-config yes
```
To upgrade your annotations database
```
humann_databases --download utility_mapping full $INSTALL_PATH --update-config yes
```
## __5. Run MetaPhlAn and HUMAnN (slurm job script example)__

```
#!/bin/bash
#SBATCH --job-name=sampleA_biobakery
#SBATCH --output=${STUDY_PATH}/QCd_reads/biobakery_stdout/sampleA_biobakery.stdout
#SBATCH --error=${STUDY_PATH}/QCd_reads/biobakery_stderr/sampleA_biobakery.stderr
#SBATCH --account=rrg-yourpi
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=17
#SBATCH --mem=64G

module load StdEnv/2020 python/3.11.2 gcc/11.3.0 diamond/2.1.6 bowtie2/2.4.4
source $INSTALL_PATH/metaphlan_env/bin/activate

cd $SLURM_TMPDIR
cp ${STUDY_PATH}/QCd_reads/sampleA_QCd/sampleA_QCd.fq.gz .

metaphlan sampleA_QCd.fq.gz --input_type fastq -o sampleA_taxa_profile.tsv --bowtie2db $INSTALL_PATH
deactivate

source $INSTALL_PATH/humann_env/bin/activate
humann -i sampleA_QCd.fq.gz -o humann_res --taxonomic-profile sampleA_taxa_profile.tsv

mkdir -p ${STUDY_PATH}/biobakery_res/sampleA_biobakery
cp -r humann_res ${STUDY_PATH}/biobakery_res/sampleA_biobakery
cp sampleA_taxa_profile.tsv ${STUDY_PATH}/biobakery_res/sampleA_biobakery/humann_res/sampleA_taxa_profile.tsv
```
[Global workflow](../README.md#global-workflow)
