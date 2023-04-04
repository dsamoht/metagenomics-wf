# Metagenomics workflow
A step-by-step guide to produce different data types derived from second generation, short reads, metagenomics sequencing.

> *__Note__* : this workflow is made to be executed on the Alliance clusters

## Setup

Suggested directory layout:

```
study_reads
├── QCd_reads
└── raw_reads
    ├── sample1_R1_001.fastq.gz
    ├── sample1_R2_001.fastq.gz
    ├── sample2_R1_001.fastq.gz
    ├── sample2_R2_001.fastq.gz
    ├── sample3_R1_001.fastq.gz
    └── sample3_R2_001.fastq.gz
```
Let's use $STUDY_PATH as the /path/to/study_reads
```
STUDY_PATH=/path/to/study_reads
```

## Global workflow

*__Inputs__*: Demultiplexed samples reads

<div align="center">

<br />

#### 1. [Quality control](/doc/run_YAMP.md)  

&#8595;

#### 2. [Assembly](doc/run_megahit.md) | [Reads mapping for taxonomy and functions](/doc/run_metaphlan_humann.md) (independent steps)

&#8595;

#### 3. [Gene prediction and translation](doc/run_prodigal.md)  

&#8595;

#### 4. [Clusters of orthologous groups of proteins (COGs)](doc/run_cdhit.md)

&#8595;

#### 5. [COG-derived data types](README.md)  

<br />

</div>

*__Outputs__*: Taxonomical and functional profiles, *de novo* assemblies and COGs matrices