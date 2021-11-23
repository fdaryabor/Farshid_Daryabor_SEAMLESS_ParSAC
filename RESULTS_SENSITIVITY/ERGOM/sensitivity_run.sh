#! /bin/bash

source common_sensitivity.sh

for period in $LIST_PERIOD ; do
        echo run ${period}
	pickle_file=${MODEL}_${SITE}_sensitivity_${period}.pickle
        echo picklefile $pickle_file
        sbatch --export=ALL,pickle_file=$pickle_file run_observability_template.sbatch
done
