#! /bin/bash


source common_sensitivity.sh

for period in $LIST_PERIOD ; do
        echo sample ${period}
        WRKDIR=$CINECA_SCRATCH/${MODEL}_${SITE}_${period}_SENSITIVITY
        pickle_file=${MODEL}_${SITE}_sensitivity_${period}.pickle
        xml_file=${SITE}_sensitivity_${period}.xml
	echo xmlfile $xml_file
	echo picklefile $pickle_file
        rm -rf $WRKDIR/????
        rm -rf $WRKDIR/?????
        parsac sensitivity sample $xml_file $pickle_file --dir $WRKDIR random 100
done

