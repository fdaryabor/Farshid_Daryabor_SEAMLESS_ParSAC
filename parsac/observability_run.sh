#! /bin/bash

source common.sh

for period in $LIST_PERIOD ; do
    for obs in $LIST_OBSERVABLE; do
        echo run ${period} ${obs}
        pickle_file=${MODEL}_${SITE}_observability_${obs}_${period}.pickle
        echo picklefile $pickle_file
        sbatch --export=ALL,pickle_file=$pickle_file run_observability_template.sbatch
    done
done

