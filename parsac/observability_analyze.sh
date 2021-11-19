#! /bin/bash
source common.sh

for period in $LIST_PERIOD ; do
    for obs in $LIST_OBSERVABLE; do
        echo analyze ${period} ${obs}
        pickle_file=${MODEL}_${SITE}_observability_${obs}_${period}.pickle
        pickle_file_analyze=${MODEL}_${SITE}_observability_${obs}_${period}.analyze.pickle
        echo picklefile $pickle_file
	file_txt=${MODEL}_${SITE}_${period}_${obs}_Observability.txt
#       parsac sensitivity analyze $pickle_file cv  > $OUTDIR/$file_txt
        parsac sensitivity analyze $pickle_file --pickle=$pickle_file_analyze cv  > $OUTDIR/$file_txt
	cp $pickle_file $OUTDIR/
        cp $pickle_file_analyze $OUTDIR/
    done
done

