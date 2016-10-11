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

## Install dependencies
Caffe has different dependencies which are required by its structure. In the following subsections an abstract list of these dependencies and the commands for installing them are provided. Depending on the available installed packages on the system, more or less dependencies might be required.

The Caffe installation in this documentation uses the build-in python of the Ubuntu-Trusty(14.04). However Anaconda-based installation can be performed but it is not required as for the moment it has more incompatibilies and may make the installation more complicated.

### Installing git, BLAS and unzip
BLAS can be used as the backend of matrix and vector computations of Caffe. There are different implementations of this library. [OpenBLAS](http://www.openblas.net/) has been chosed. 
```
sudo apt-get install libopenblas-dev git unzip
```
Alternatively you can refer to [OpenBLAS repository](https://github.com/xianyi/OpenBLAS).

### Install OpenCV
The [OpenCV](https://help.ubuntu.com/community/OpenCV) is the well-known open-source computer vision library.

There are three suggested way for installing OpenCV.
1. Install directly using the [this file](https://github.com/astorfi/Caffe_Framework/blob/master/Installation/OpenCV_Installation/OpenCV.sh) available in this repository.

2. Install directly using the [second file](https://github.com/astorfi/Caffe_Framework/blob/master/Installation/OpenCV_Installation/OpenCV.sh) available in this repository.

3. Install as follows for the particular version:
```
wget https://raw.githubusercontent.com/jayrambhia/Install-OpenCV/master/Ubuntu/2.4/opencv2_4_9.sh
chmod +x opencv2_4_9.sh 
./opencv2_4_9.sh
```
* The first two files are the edited version of the second method.

4. Install using the source from the [this guide]http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/.

### Install other dependecies(Boost,...)
```
sudo apt-get install libboost-all-dev
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev
sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler
```

### Install protobuf

For protobuf installation, simple pip installation is recommended.
```
pip install protobuf
```


