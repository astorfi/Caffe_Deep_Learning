# Caffe Installation 

The step by step processes of caffe installation in `Ubuntu(14.04)` is provided here. 

### Hardware & cuda version
The following installation has been implemented and successfully tested on [CUDA 8.0](http://on-demand.gputechconf.com/gtc/2016/webinar/cuda-8-features-overview.pdf) and [NVIDIA TITAN X(Pwered by Pascal) GPU](http://www.geforce.com/hardware/10series/titan-x-pascal). However the method can simply be used for older version of `CUDA` and older `GPU architectures`.

### CUDA installation

For the [NVIDIA TITAN X(Pwered by Pascal) GPU](http://www.geforce.com/hardware/10series/titan-x-pascal), installing CUDA 8.0 is necessary. The CUDA 8.0 download file and installation procedure can be found [here](https://developer.nvidia.com/cuda-downloads). The system platform has to be chosen as the following image: ![](Images/Select Target Platform.png).

First using the terminal go to the folder that the downloaded `.deb` file is located. Now the installation has to be done as follows:

```
sudo dpkg -i cuda-repo-ubuntu1404-8-0-local_8.0.44-1_amd64.deb
sudo apt-get update
sudo apt-get install cuda
```

It is worth mentioning that, the described procedure is the straight-forward approach of installing CUDA. Issues like `black screen`, `stuck in login page` and other incompatibilities may happen which are beyond the scope of this documentation.


### Preinstallation and CUDA compatibility
Now the assumption is that the [CUDA](http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#axzz4MnU6Gq6E) is already installed.

Check the supporting GPU(s) and Ubuntu version using the following command:

```
lspci | grep -i nvidia
uname -m && cat /etc/*release
 gcc --version
```

## Python Installation
Caffe has different dependencies which are required by its structure. In the following subsections an abstract list of these dependencies and the commands for installing them are provided. Depending on the available installed packages on the system, more or less dependencies might be required.

The Caffe installation in this documentation uses the build-in python of the 'Ubuntu-Trusty(14.04)'. However 'Anaconda-based' installation can be performed but it is not required as for the moment it has more incompatibilies and may make the installation more complicated.

**WARNING:** make sure the `Python` recognized by the system is the `default built-in Python` by the ubuntu and *Anaconda does not own the path* for python. You can check that with the following command which returns the root pf python:

```
which python
```
Basically you need to check that the Anaconda is not installed or the `default Python` does not belongs to the `Anaconda path`. With this check-up you can make sure that the `Caffe` installation does not point to the wrong path. This step is crucial for using `Python interface` of the `Caffe`.

### Installing git, BLAS and unzip
`BLAS` can be used as the backend of matrix and vector computations of Caffe. There are different implementations of this library. [OpenBLAS](http://www.openblas.net/) has been chosed. 
```
sudo apt-get install libopenblas-dev git unzip
```
Alternatively you can refer to [OpenBLAS repository](https://github.com/xianyi/OpenBLAS).

### Install OpenCV
The [OpenCV](https://help.ubuntu.com/community/OpenCV) is the well-known open-source computer vision library.

There are three suggested way for installing OpenCV.

#### Using bash script files
1. Install directly by going to [this link](https://github.com/astorfi/Caffe_Framework/tree/master/Installation/OpenCV_Installation) and using one of the "OpenCV.sh" or "OpenCV_Alternative.sh" bash script files available in this repository.
 * The second file is more abstract and installs less dependancies. This may lead to have less conflicts and incompatibilties.
2. Install as follows for the particular version:
 * The first two files are the edited version of the second method.
```
wget https://raw.githubusercontent.com/jayrambhia/Install-OpenCV/master/Ubuntu/2.4/opencv2_4_9.sh
chmod +x opencv2_4_9.sh 
./opencv2_4_9.sh
```
However by using this method, [unsupported gpu architecture](http://stackoverflow.com/questions/28010399/build-opencv-with-cuda-support) error has been reported. Most like this is due to requirements of some `OpenCV` installations to define the "CUDA_GENERATION" explicitly.
#### Install from the source
Install using the source from the [source](http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html)

### Install other dependecies(Boost,...)
```
sudo apt-get update
sudo apt-get install python-skimage
sudo apt-get install libboost-all-dev
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev
sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler
sudo apt-get install libatlas-base-dev
```

### Install protobuf

For protobuf installation, simple `pip installation` is recommended.
```
pip install protobuf
```

You may need to install `pip` before installation of the `protobuf`.

### Clone and Install Caffe from Source
In this phase, the Caffe repository must be cloned and install:

```
git clone https://github.com/BVLC/caffe
```

After going to code directory, a copy of `Makefile.config.example` file under the new name of `Makefile.config` must be make to be modified if necessary.
```
cd caffe
cp Makefile.config.example Makefile.config
```
For making any modification, the `Makefile.config` must be edited. Here's are few possible modifications:

* The CuDNN can be activated using the assigned flag.
* Instead of Python, Anaconda can be used by changing the associated paths.
* The default is using GPU but if the "CPU_ONLY := 1" is activated, then there is no GPU support!

In the end we can compile and make all the test files:
```
make all
make test
```
It is worth mentioning that `-jX` command can be added to the above commands to increase the speed of process. `X` is the 
number of supported CPU cores.

### Installing Pycaffe
For having a python interface for the caffe use the following:
```
cd python
for req in $(cat requirements.txt); do sudo pip install $req; done
cd ..
make pycaffe
```
In the above terminal commands the assumption is that we are in the `$CAFFE_ROOT`. The `sudo` part is to overcome the
`permission denied` issue while installing dependencies. However adding `sudo` has not been mentioned as part of the
documentation provided by the [official Caffe installation](http://caffe.berkeleyvision.org/installation.html#prerequisites), it demonstrated incompatibility by ignoring `sudo`.

WARNING: The above requirement must be installed in the default python which is in the root otherwise the cannot be recognized by the `pycaffe`. However using the command `sudo apt-get install python-skimage` probably immune the installation from its last part which is installing the dependencies defined in the `requirements.txt` file.

In the end we can run all the tests:
```
make runtest
```

### Alternatinve Method

Another way for considering the procedure of the installation is to to the following:
```
cd python
for req in $(cat requirements.txt); do sudo pip install $req; done
cd ..
```

Then make all the necessary elements:
```
make all
make pycaffe
make test
make runtest
```

Now add the following to the `source bash file`:
```
export CAFFE_ROOT=/path/to/caffe (ex: /home/username/caffe)
export PYTHONPATH=$CAFFE_ROOT/python:$PYTHONPATH
```

### Installation check

By using the following command check if the `Caffe` is already installed and can be loaded by `Pycaffe`:
```
python
import caffe
```

**CAVEAT:** If you cannot import `Caffe` that does not mean `Caffe` is not installed! Passing all tests in the previous phase
guaranties the success of installation `Caffe`. However not being able to import caffe after running python is related to the pycaffe interface.

### Reported Issue
Then it might be necessary to copy appropriete files be copied in order to prevent [this issue](https://github.com/BVLC/caffe/issues/1463).
```
sudo cp libhdf5_hl.so.7 libhdf5_hl.so.8
sudo cp libhdf5.so.7 libhdf5.so.8
```


## Anaconda Installation

At this moment the assumption is that the user wants to install `Anaconda` and use the `Caffe`. So after `Python Installation Procedure`, few modifications must be done.

### Download

Anaconda must be downloaded from its [website](https://www.continuum.io/downloads). `Anaconda Python 2.7` is recommended.

### Editing the bash file

The following two command should be added to the end of `source bash file`. However based on the experiments the necessity of the second one has not been proven! 
```
export PATH="/home/sina/anaconda/bin:$PATH"
export LD_LIBRARY_PATH=/home/sina/anaconda/lib:$LD_LIBRARY_PATH

```

### Installing protobuf
The protobuf should be installed this time using `conda`:
```
conda install protobuf
```

## Using Pycharm or other IDEs

In order to use the IDE and importing Caffe, The IDE(ex: Pycharm) *must be run from the terminal*.


