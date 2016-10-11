This folder is related to OpenCV installation which is a dependecy for the Caffe.

Here's is the procedure and considerations:

1. Download and run the "OpenCV.sh" file for installing OpenCV.
2. Installing "ffmpeg" can be ignore for two reason:
  * the package might not be available in Ubuntu(14.04) 
  * Other possible incompatibilities.
  * "ffmpeg" can be installed from the source in a more eficient way.
3. In the "OpenCV.sh" file the command "make -j16" in line 17 is for using all the CPUs(speed up the process). In the part -jX, X is dependent to the number of CPUs supported by the system.

**If the "OpenCV.sh" file has some issues you can alternatively install "OpenCV_Alternative.sh" file.**
