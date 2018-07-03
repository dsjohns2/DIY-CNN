import os

vid_files = os.listdir("../../videos")
for vid_file in vid_files:
	if(vid_file.endswith(".mp4")):
		dir_name = vid_file.split("/")
		dir_name = dir_name[-1]
		dir_name = dir_name.split(".")[0]
		os.makedirs(dir_name + "_images")
