# Caffe Installation 

The step by step processes of caffe installation in Ubuntu(14.04) is provided here. 

## Hardware & cuda version
The following installation has been implemented and successfully tested on [CUDA 8.0](http://on-demand.gputechconf.com/gtc/2016/webinar/cuda-8-features-overview.pdf) and [NVIDIA TITAN X(Pwered by Pascal) GPU](http://www.geforce.com/hardware/10series/titan-x-pascal).

## Preinstallation and CUDA compatibility
The assumption is that the [CUDA](http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#axzz4MnU6Gq6E) is already installed.

Check the supporting GPU and the version using the following command:
'''
lspci | grep -i nvidia
uname -m && cat /etc/*release
 gcc --version
'''
