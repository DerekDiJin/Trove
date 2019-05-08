#!/bin/bash

echo 'Start running s3'

for i in {0..39}
do
	init_line=$(( 5000000*i ))
	end_line=$(( 5000000*(i+1) ))
	echo  $init_line #'$i' * 5000000
	echo $end_line

	output_file='Trove_depth_pid_temporal_p'$i'.tsv'
	echo $output_file

	python s3_eid2pid.py Trove_depth_1hops_eid_temporal.tsv $output_file $init_line $end_line
	sleep 10
done

echo 'Script ends.'