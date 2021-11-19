#! /bin/bash

REFDIR=/g100_work/tra21_seamless/RESULTS_ONEYEAR/
REFDIR=/g100_scratch/usertrain/a08trb34/RESULTS_ONEYEARat/


SITE=BATS

python plot_timeseries_indicators_ALL.py -s $SITE -i $REFDIR

python plot_timeseries_observations_ALL.py -s $SITE -i $REFDIR

cp *_${SITE}_oneyear*png ${REFDIR}/

