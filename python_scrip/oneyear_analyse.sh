#! /bin/bash

REFDIR=/g100_work/tra21_seamless/RESULTS_ONEYEAR/

MODEL=ERGOM

SITE=BATS
INFILE=/g100_work/tra21_seamless/RESULTS_ONEYEAR/ERGOM/ERGOM_BATS_ANNUAL_result.nc

#python indicators_timeseries_bats.py -i $INFILE -m $MODEL
#cp ${MODEL}_${SITE}_ONEYEAR_INDICATORS.txt ${REFDIR}/${MODEL}/
#python plot_timeseries_indicators.py -s $SITE -m $MODEL -i $REFDIR

#python observations_timeseries_bats.py -i $INFILE -m $MODEL
#cp ${MODEL}_${SITE}_ONEYEAR_OBSERVATIONS.txt ${REFDIR}/${MODEL}/
#python plot_timeseries_observations.py -s $SITE -m $MODEL -i $REFDIR

#cp ${MODEL}_${SITE}_oneyear*png ${REFDIR}/${MODEL}/

SITE=L4
INFILE=/g100_work/tra21_seamless/RESULTS_ONEYEAR/ERGOM/ERGOM_L4_ANNUAL_result.nc

#python indicators_timeseries_L4.py -i $INFILE -m $MODEL
#cp ${MODEL}_${SITE}_ONEYEAR_INDICATORS.txt ${REFDIR}/${MODEL}/
#python plot_timeseries_indicators.py -s $SITE -m $MODEL -i $REFDIR

#python observations_timeseries_L4.py -i $INFILE -m $MODEL
#cp ${MODEL}_${SITE}_ONEYEAR_OBSERVATIONS.txt ${REFDIR}/${MODEL}/
#python plot_timeseries_observations.py -s $SITE -m $MODEL -i $REFDIR

#cp ${MODEL}_${SITE}_oneyear*png ${REFDIR}/${MODEL}/
