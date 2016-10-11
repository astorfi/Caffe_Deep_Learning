# Caffe Installation 
[link](https://gist.github.com/titipata/f0ef48ad2f0ebc07bcb9)
[Link2](http://stackoverflow.com/questions/24479060/ubuntu-12-04-ld-cannot-find-library)
[Link3](https://github.com/BVLC/caffe/issues/559)

The step by step processes of caffe installation in Ubuntu(14.04) is provided here. 

## Hardware & cuda version
The following installation has been implemented and successfully tested on [CUDA 8.0](http://on-demand.gputechconf.com/gtc/2016/webinar/cuda-8-features-overview.pdf) and [NVIDIA TITAN X(Pwered by Pascal) GPU](http://www.geforce.com/hardware/10series/titan-x-pascal).

## CUDA installation

For the [NVIDIA TITAN X(Pwered by Pascal) GPU](http://www.geforce.com/hardware/10series/titan-x-pascal), installing CUDA 8.0 is necessary. The CUDA 8.0 download file and installation procedure can be found [here](https://developer.nvidia.com/cuda-downloads). The system platform has to be chosen as the following image: ![](Images/Select Target Platform.png).

First using the terminalgo to the folder that the downloaded ".deb" file is located. Now the installation has to be done as follows:

```
sudo dpkg -i cuda-repo-ubuntu1404-8-0-local_8.0.44-1_amd64.deb
sudo apt-get update
sudo apt-get install cuda
```

It is worth mentioning that, the described procedure is the straight-forward approach of installing CUDA. Issues like "black screen", "stuck in login page" and other incompatibilities may happen which are beyond the scope of this documentation.


## Preinstallation and CUDA compatibility
Now the assumption is that the [CUDA](http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#axzz4MnU6Gq6E) is already installed.

Check the supporting GPU(s) and Ubuntu version using the following command:

```
lspci | grep -i nvidia
uname -m && cat /etc/*release
 gcc --version
```




