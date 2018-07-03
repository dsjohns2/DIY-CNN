#!/bin/bash

# Generate Data
cd data/generate_data
./generate_data.sh

# Train Network
cd ../..
num_vids=$(ls -1q ./videos/*.mp4 | wc -l)
python generate_model.py $num_vids
python test_model.py $num_vids

# Run Network on Video Stream
cd run_on_stream
python run_model.py $num_vids
