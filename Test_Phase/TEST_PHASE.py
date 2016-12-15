import os
import glob
import sys
import multiprocessing
from sklearn import preprocessing
import lmdb
import numpy as np
import caffe
import cv2
from caffe.proto import caffe_pb2
from sklearn import metrics
import scipy.io as sio
import matplotlib.pyplot as plt
import random
from PyQt4.QtGui import *
from PySide import QtGui, QtCore
from easygui import *
from TEST_PHASE_Functions import *

"""
GUI PART
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
task_title = 'You want to see the results for training or testing?!'
form = MyButtons(choices=user_options, title=task_title)
form.exec_()
choice_phase = form.choice

if choice_phase == "TRAIN":
    LMDB_FILE_NAME = '/home/sina/caffe/TrainModels/Siamese/SiameseCNN/DATA/TWIN/pairs_twins_train_224x224_lmdb'
elif choice_phase == "TEST":
    LMDB_FILE_NAME = '/home/sina/caffe/TrainModels/Siamese/SiameseCNN/DATA/TWIN/Image_TEST_test_id_2014_2015_joint_unseen-2010to2013'
# If user canceled the operation.
elif choice_phase == 'Cancel':
    sys.exit("Canceled by the user")

# Forward passing mean if you want to feed the data to network and see the output of any layer!
user_options = ['YES', 'NO', 'Cancel', 'Continue']
task_title = 'Do want to perform the forward passing to network??!'
form = MyButtons(choices=user_options, title=task_title)
form.exec_()
choice_passing = form.choice

if choice_passing == "YES":
    choice_netwrok = 'forward_passing'
elif choice_passing == "NO":
    choice_netwrok = 'input_visualization'
# If user canceled the operation.
elif choice_passing == 'Cancel':
    sys.exit("Canceled by the user")


# Forward passing mean if you want to feed the data to network and see the output of any layer!
user_options = ['YES', 'NO', 'Cancel', 'Continue']
task_title = 'Do want to Visualize the ROC curve and histogram??!'
form = MyButtons(choices=user_options, title=task_title)
form.exec_()
choice_visualize = form.choice

"""
Calling the structure
"""
np.set_printoptions(threshold=np.nan)
caffe.set_device(1)
caffe.set_mode_gpu()

# Necessary file calling
MODEL_FILE = 'test_performance.prototxt'
# PRETRAINED_MODEL = '/home/sina/caffe/TrainModels/Siamese/SiameseCNN/DATA/weights/casia_train_224x224_iter_100000.caffemodel'
PRETRAINED_MODEL = '/home/sina/caffe/TrainModels/Siamese/SiameseCNN/DATA/weights/twins_train_224x224_iter_25000.caffemodel'


# Activating the fowrad pass towards the network.
if choice_netwrok == 'forward_passing':
    # Creating net
    net = caffe.Net(MODEL_FILE, PRETRAINED_MODEL, caffe.TEST)

# Opening LMDB file
lmdb_env = lmdb.open(LMDB_FILE_NAME)
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe_pb2.Datum()

# Calculate number of files.
num_img = 0
for key, value in lmdb_cursor:
    num_img += 1
label = []
distance = np.zeros((num_img, 1))
loss = np.zeros((num_img, 1))
similarity = np.zeros((num_img, 1))
print "Number of pairs: %d ", num_img

# Going through all files in LMDB file
original_features = []
counter = 0
for key, value in lmdb_cursor:
    datum.ParseFromString(value)

    # Getting the label and data
    label.append(int(datum.label))
    pair_features = caffe.io.datum_to_array(datum)
    original_features.append(pair_features)

    if choice_netwrok == 'forward_passing':

        # Feeding the data.
        net.blobs['data'].data[...] = pair_features

        # Fowrard passing
        out = net.forward()
        loss[counter] = out['loss'] # Calculated by the caffe: (np.sum(np.square(out_1 - out_2))) / 2

        out_1 = net.blobs['fc7'].data
        out_2 = net.blobs['fc7_p'].data

        # # Calculate output distance metric Manually(Warning!! This is the same implementation by the caffe for batch_size = 1)
        distance[counter] = np.sqrt((np.sum(np.square(out_1 - out_2))))


    counter = counter + 1
    if counter % 100 == 0:
        print("The %d - th data passed!" % counter)


"""
PART1: Output of the Network.
"""

if choice_netwrok == 'forward_passing':

    # TODO: K-Flod validation.
    EER_VALIDATION, AUC_VALIDATION = K_Fold_Validation(label, distance, k=5)

    if choice_visualize == 'YES':

        # Plot histogram.
        Plot_HIST_Fn(label, distance, choice_phase, 'Siamese_Output_Histogram.jpg')

        # Plot ROC
        Plot_ROC_Fn(label, distance, choice_phase, 'Siamese_Output_ROC.jpg')

"""
PART2: Plotting the histogram of original features and the ROC curve
"""

## Calculation of the original input distances.
distance_original = np.zeros([len(original_features), 1])
for i in range(len(original_features)):
    # Euclidean loss
    distance_original[i] = np.sqrt(np.sum(np.square(original_features[i][:, :, 0] - original_features[i][:, :, 1])))    # L2 - norm

if choice_visualize == 'YES':
    
    # Plot input histogram
    Plot_HIST_Fn(label, distance_original, choice_phase, 'OriginalFeatures_Histogram.jpg')

    # Plot input ROC
    Plot_ROC_Fn(label, distance_original, choice_phase, 'Siamese_Input_ROC.jpg')
