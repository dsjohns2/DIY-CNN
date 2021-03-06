#!/bin/bash

# Remove old data
rm *_images -r
rm ../test -r
rm ../train -r

# Create directories for new images
python gen_image_dirs.py
mkdir ../test
mkdir ../train

# Generate new images from video
./vid_to_images.sh

# Move and label data to test and train directories
python move_data.py
