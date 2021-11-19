#! /bin/bash
#SBATCH --job-name=copy-sensitivty
#SBATCH --time=4:00:00
#SBATCH --partition=g100_all_serial

cd $SLURM_SUBMIT_DIR

parsac sensitivity sample  bats_sensitivity_indicators.xml bats_sensitivity_indicators.pickle --dir /g100_work/tra21_seamless/ERGOM/SENSITIVITY_WINTER random 1680


