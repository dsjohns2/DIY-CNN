#!/bin/bash

# Run Network on Video Stream
num_vids=$(ls -1q ../videos/*.mp4 | wc -l)
python run_model.py $num_vids
