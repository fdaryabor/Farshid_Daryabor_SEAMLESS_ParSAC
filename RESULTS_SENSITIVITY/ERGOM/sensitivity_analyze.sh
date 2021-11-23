#! /bin/bash
source common_sensitivity.sh

for period in $LIST_PERIOD ; do
        echo analyze ${period} 
        pickle_file=${MODEL}_${SITE}_sensitivity_${period}.pickle
        pickle_file_analyze=${MODEL}_${SITE}_sensitivity_${period}.analyze.pickle
        echo picklefile $pickle_file
	file_txt=${MODEL}_${SITE}_${period}_sensitivity.txt
        parsac sensitivity analyze $pickle_file --pickle=$pickle_file_analyze mvr  > $OUTDIR/$file_txt
	cp $pickle_file $OUTDIR/
        cp $pickle_file_analyze $OUTDIR/
done

