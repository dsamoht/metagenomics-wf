# Metagenomics workflow
> A protocol to produce reference-based functional and taxonomical profiles and assembly-based, gene clusters matrices.  
__keywords__: `shotgun metagenomics` | `assembly` | `biobakery` | `YAMP` | `megahit` | `prodigal` | `CD-HIT` | `slurm`

- From here, we assume that your samples have been demultiplexed
- This protocol is made to be executed on the Alliance clusters
- For simplification purposes, we apply the same treatment for all samples. Modifications might be needed if your samples origin from different studies.


## 0) Setup
Let's organized the directory containing our data:
```
study_reads
└── raw_reads
    ├── sample1_R1_001.fastq.gz
    ├── sample1_R2_001.fastq.gz
    ├── sample2_R1_001.fastq.gz
    ├── sample2_R2_001.fastq.gz
    ├── sample3_R1_001.fastq.gz
    └── sample3_R2_001.fastq.gz
```

## 1) Quality control with [YAMP](https://github.com/alesssia/YAMP)

