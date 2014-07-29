# This script launches the webcam using mjpeg-streamer. It takes the input
# as the default webcam, uses the input_uvc.so plugin and captures the
# video in 352x288 resolution at 5 fps with 100 jpg quality.
#
# The streamer is configured to have two outputs: one output streams to
# the Beaglebone web server at port 8090 and the other outputs a frame to a file
# at the mjpg-streamer/mjpg-streamer/pics folder every 550ms. This folder
# keeps 3 files at a time and after every file is saved, the script
# image_ready.py is executed.
#
# Created by Stephen Arifin
# July 28th, 2014

sudo ./mjpg-streamer/mjpg-streamer/mjpg_streamer -i "./mjpg-streamer/mjpg-streamer/input_uvc.so -d /dev/video0 -n -r 352x288 -y -f 5 -q 100" -o "./mjpg-streamer/mjpg-streamer/output_http.so -p 8090 -w ./www" -o "./mjpg-streamer/mjpg-streamer/output_file.so -f ./mjpg-streamer/mjpg-streamer/pics -d 150 -s 3 -c ./image_ready.py"
