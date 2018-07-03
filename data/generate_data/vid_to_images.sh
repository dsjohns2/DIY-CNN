#!/bin/bash

# Create new images from video
for video_name in ../../videos/*.mp4;
do
	label="${video_name##*/}"
	label="${label%.*}"
	ffmpeg -i $video_name -ss 00:00:02 -r 15 ./${label}_images/%04d.jpg
done

# Resize new images
for path in *_images/;
do
	for image in $( ls $path);
	do
		image_path="$path$image"
		convert $image_path -resize 32x32\! $image_path
	done
done
