#!/bin/bash

echo 'Start running s3_split'

for filename in Trove_depth_1hops_eid_temporal_dir/*
do
	echo $filename

	output_file=$filename'_p.tsv'
	echo $output_file

	python s3_eid2pid.py $filename $output_file
	sleep 10
done

echo 'Script ends.'