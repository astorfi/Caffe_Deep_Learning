# Create LMDB

This part is to provide instructions of how to create LMDB file dormat which is supported by the Caffe and to the best of our knowledge 
it is the most compatible file format with the Caffe and provides fastest processing among all other type, i.e., HDF5 and etc.

The are two general ways to cerate LMDB file. One is to use [numpy](http://www.numpy.org/) file format as the imput and python for creating the LMDB. The alternative and faster way is to use shell file and raw images(with .png or .jpg format) as the input.

## Using Numpy file format

For creating file format from numpy files it is clear that all the files whether of image raw pixels or feature or basically what ever elements that should be stored in LMDB file, must have numpy(.npy) format. The python file for creating LMDB file from numpy is provided here.
