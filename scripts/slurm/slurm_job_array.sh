#!/bin/bash
#SBATCH --array=1-63

DIR=/home/jefor184/projects/def-jcomte/jefor184/EcoBiomics_Hiseq/scripts/yamp # Directory containing the job scripts
file=`ls $DIR | awk -vid="$SLURM_ARRAY_TASK_ID" 'NR == id'`
sbatch $DIR/$file
