
import os
import glob
import sys
import multiprocessing
import random
import dircache
import lmdb
import numpy as np
import caffe
from caffe.proto import caffe_pb2
from PyQt4.QtGui import *
from PySide import QtGui, QtCore
import cv2

"""
This file creates an LMDB file from numpy files. The application is face varification in which the
LMDB file will be created from pairs of images. The genuine pairs get label "1" and the imposter
pairs get label "0". The genuine files contains "gen" in their file name.

For this process, the numpy files are features
but they basically can be anything saved in numpy files.

This file do the following:
1 - load all the ".npy" data from a folder and create a big numpy array
    * The numpy files initially have the format of (Width, height, num_channels, 2) and 2 is due to having pairs.
      Change the dimensions along this code as required by your specific file shape.
2 - Create an LMDB file from that numpy array
"""

"""
GUI Class definition
"""


class MyButtons(QtGui.QDialog):
    """"""

    def __init__(self, choices, title):
        # Initialized and super call.
        super(MyButtons, self).__init__()
        self.initUI(choices, title)
        self.choice = choices

    def initUI(self, choices, title):
        option1Button = QtGui.QPushButton(choices[0])
        option1Button.clicked.connect(self.onOption1)
        option2Button = QtGui.QPushButton(choices[1])
        option2Button.clicked.connect(self.onOption2)
        option3Button = QtGui.QPushButton(choices[2])
        option3Button.clicked.connect(self.onOption3)
        option4Button = QtGui.QPushButton(choices[3])
        option4Button.clicked.connect(self.onOption4)

        buttonBox = QtGui.QDialogButtonBox()
        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttonBox.addButton(option1Button, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(option2Button, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(option3Button, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(option4Button, QtGui.QDialogButtonBox.ActionRole)
        #
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)
        # define window		xLoc,yLoc,xDim,yDim
        self.setGeometry(250, 250, 100, 100)
        self.setWindowTitle(title)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def onOption1(self):
        self.retStatus = 1
        self.close()
        self.choice = self.choice[0]

    def onOption2(self):
        self.retStatus = 2
        self.close()
        self.choice = self.choice[1]

    def onOption3(self):
        self.retStatus = 3
        self.close()
        self.choice = self.choice[2]

    def onOption4(self):
        self.retStatus = 4
        self.close()
        self.choice = self.choice[3]


"""
GUI for training or testing phase.
"""
app = QtGui.QApplication(sys.argv)
user_options = ['TRAIN', 'TEST', 'Cancel', 'Continue']
task_title = 'Are you intended to create testing or training pairs?!'
form = MyButtons(choices=user_options, title=task_title)
form.exec_()
choice_phase = form.choice

# If user canceled the operation.
if choice_phase == 'Cancel':
    sys.exit("Canceled by the user")

"""
GUI for getting the type of features.
"""
user_options = ['Image', 'HOG', 'LBP', 'none']
task_title = 'From which kind of features you want to create pairs?!'
form = MyButtons(choices=user_options, title=task_title)
form.exec_()
choice_feature = form.choice

"""
GUI for getting the type of features.
"""
user_options = ['Yes', 'No', 'DC', 'none']
task_title = 'mean subtraction by channel?!'
form = MyButtons(choices=user_options, title=task_title)
form.exec_()
choice_mean = form.choice

# Source and destination paths(both with absolute path).
this_path = os.path.dirname(os.path.abspath(__file__))
# This path definition is specific. Change it as needed.
src_folder_path = 'Path/to/root/source' + choice_feature + '/' + choice_phase   
dst_folder_path = choice_feature + '_' + choice_phase + '_' + 'train-2010to2013-unique'

# # Getting the number of cores for parallel processing
# num_cores = multiprocessing.cpu_count()
# print('Total number of cores', num_cores)

# Getting the number of files in the folder
num_files = (len([name for name in os.listdir(src_folder_path) if os.path.isfile(os.path.join(src_folder_path, name))]))
print("Number of files = ", num_files)

# Read a random file for getting the shapes.
RandFile = random.choice(dircache.listdir(src_folder_path))
FileShape = np.load(os.path.join(src_folder_path,RandFile)).shape
print("File shape: ", FileShape)


# This part is specific for the feature cube of pairs that been generated.
N = num_files
X = np.zeros((N, FileShape[2], FileShape[0], 2 * FileShape[1]), dtype=np.int64) # the number 2 is because the hog features of a pairs should be considered separately
y = np.zeros(N, dtype=np.int64)
FileNum = np.zeros(N, dtype=np.int64)

# Initialize a counter.
counter = 0

# We should shuffle the order to save the files in LMDB format.
Rand_idx = np.random.permutation(range(N))
mean_image = np.load('mean_image.npy')
mean_image = np.transpose(mean_image, (2, 0, 1))
mean_image = np.mean(mean_image, axis=(1,2))


# Reading all the numpy files
for f in glob.glob(os.path.join(src_folder_path, "*.npy")):
    # Load numpy file
    numpy_array = np.load(f)

    # # Uncomment if the files have naming order and you want to save the naming order too.
    # file_num = os.path.basename(os.path.basename(f).split('_')[1]).split('.')[0]    # This gets the number of file
    # FileNum[Rand_idx[counter]] = file_num

    # Save to new big vector X.(since numpy reshape does not preserve the order, we put all by hand!!)
    # FOr caffianeting the data, the second dimension in the data blob should be the channel!

    # Initial format
    left = numpy_array[:, :, :, 0]
    right = numpy_array[:, :, :, 1]

    # Change format
    # The format supported by Caffe is (Num_Samples, Num_Channels, Width, Height).
    # Comment this part if you already have the numpy files with the correct format.
    left = np.transpose(left, (2, 0, 1))
    right = np.transpose(right, (2, 0, 1))

    if choice_mean == 'Yes':
        left[0, :, :] = left[0, :, :] - mean_image[0]
        left[1, :, :] = left[1, :, :] - mean_image[1]
        left[2, :, :] = left[2, :, :] - mean_image[2]

        right[0, :, :] = right[0, :, :] - mean_image[0]
        right[1, :, :] = right[1, :, :] - mean_image[1]
        right[2, :, :] = right[2, :, :] - mean_image[2]

    X[Rand_idx[counter], :, :, :224] = left
    X[Rand_idx[counter], :, :, 224:] = right


    # If the pairs is genuine, then it has a "gen" in its name.
    if 'gen' in f:
        y[Rand_idx[counter]] = 1
    if counter % 100 == 0:
        # print("Processing file: {}".format(f))
        print("Processing %d pairs" % counter)
    counter = counter + 1

# # This part is commented due to memory problem for large data.
# # Create a big array in order to turn into LMDB
# X = np.delete(X, np.s_[counter:X.shape[0]],0)  # delete extra pre-allocated space

# LMDB GENERATION
ExtraMem = 100000   # Rule of thumb: the bigger the better if not out of memory!!
env = lmdb.open(dst_folder_path, map_size=ExtraMem * counter)

lmdb_file = dst_folder_path
batch_size = 256
number_of_batches = np.ceil(num_files/batch_size).astype(int)

lmdb_env = lmdb.open(lmdb_file, map_size=int(1e12))
lmdb_file = lmdb_env.begin(write=True)
datum = caffe_pb2.Datum()

batch_num = 1
file_to_LMDB_num = 0
for i in range(N):

    # prepare the data and label
    # .astype(np.uint8) is for creating int instead of float for
    # faster postprocessing if we don't want any mean subtraction or etc.
    data = X[i,:,:,:].astype(np.uint8)
    label = int(y[i])

    # save in datum
    datum = caffe.io.array_to_datum(data, label)
    key = '{:0>8d}'.format(file_to_LMDB_num)
    lmdb_file.put(key, datum.SerializeToString())

    # write batch(batch size is flexible)
    if file_to_LMDB_num % batch_size == 0 and file_to_LMDB_num > 0:
        lmdb_file.commit()
        lmdb_file = lmdb_env.begin(write=True)
        print ("Generating batch {} of {}".format(batch_num,number_of_batches))
        batch_num += 1

    # Increasing the counter
    file_to_LMDB_num += 1

# write last batch(because the number of files cannot be necessary divisive by the batch size)
if (file_to_LMDB_num) % batch_size != 0:
    lmdb_file.commit()
    print('generating last batch ...')
    print(file_to_LMDB_num)
