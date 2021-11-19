#! /bin/bash


source common.sh

for period in $LIST_PERIOD ; do
    for obs in $LIST_OBSERVABLE; do
        echo sample ${period} ${obs}
        WRKDIR=$CINECA_SCRATCH/${MODEL}_${SITE}_${period}_${obs}_OBSERVABILITY
        pickle_file=${MODEL}_${SITE}_observability_${obs}_${period}.pickle
        xml_file=${SITE}_observability_${obs}_${period}.xml
	echo xmlfile $xml_file
	echo picklefile $pickle_file
        rm -rf $WRKDIR/????
        rm -rf $WRKDIR/?????
        parsac sensitivity sample $xml_file $pickle_file --dir $WRKDIR random 100
    done
done

