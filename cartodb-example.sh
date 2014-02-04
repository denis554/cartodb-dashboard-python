#!/bin/bash
echo 'IMPORTING'
#python -c 'import cartodb_api_wrapper; cartodb_api_wrapper.import_data("/Users/simonhope/data/PSMA/schools1.csv")'
./cartodb_api_wrapper.py
echo $?

#echo 'DATA TYPE CONVERSION'
#python -c 'import cartodb_api_wrapper; cartodb_api_wrapper.update_data_types("point_pid","number","schools1_20")'
#echo $?