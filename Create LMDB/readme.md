This part is to provide instructions of how to create LMDB file dormat which is supported by the Caffe and to the best of our knowledge 
it is the most compatible file format with the Caffe and provides fastest processing among all other type, i.e., HDF5 and etc.

The are two general ways to cerate LMDB file. One is to use [numpy](http://www.numpy.org/) file format as the imput and python for creating the LMDB. The alternative and faster way is to use shell file and raw images(with .png or .jpg format) as the input.
