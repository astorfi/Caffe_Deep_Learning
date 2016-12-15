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

def K_Fold_Validation(label, distance, k = 5):

    # Flipping the distance to get the dissimilarity
    similarity_output = - distance

    """
    K-Fold validation on data
    """

    # Get the fold lenth
    fold_lenth = int(len(label) / k)
    EER = np.zeros((k, 1))
    AUC = np.zeros((k, 1))

    EER_stat = []
    AUC_stat = []

    # Looping over all folds
    for itr in range(k):
        # Calculating the ROC curve
        fpr, tpr, thresholds = metrics.roc_curve(label[itr*fold_lenth:(itr+1)*fold_lenth], similarity_output[itr*fold_lenth:(itr+1)*fold_lenth], pos_label=1)

        # Calculating EER
        intersect_x = fpr[np.abs(fpr - (1 - tpr)).argmin(0)]
        EER[itr, 0] = intersect_x

        # AUC(area under the curve) calculation
        AUC[itr, 0] = np.trapz(tpr, fpr)

    EER_stat.append(np.mean(EER,axis=0))
    EER_stat.append(np.std(EER, axis=0))

    AUC_stat.append(np.mean(AUC, axis=0))
    AUC_stat.append(np.std(AUC, axis=0))

    return EER_stat, AUC_stat

def Plot_HIST_Fn(label, distance, choice_phase, save_name):

    # Plot histogram of output
    gen_dissimilarity = []
    imp_dissimilarity = []
    for i in range(len(label)):
        if label[i] == 1:
            gen_dissimilarity.append(distance[i][0])
        else:
            imp_dissimilarity.append(distance[i][0])

    bins = np.linspace(0, np.amax(distance), 50)
    fig = plt.figure()
    plt.hist(gen_dissimilarity, bins, alpha=0.5, facecolor='blue', normed=False, label='gen_dist')
    plt.hist(imp_dissimilarity, bins, alpha=0.5, facecolor='red', normed=False, label='imp_dist')
    plt.legend(loc='upper right')
    plt.show()
    fig.savefig(choice_phase + '_' + save_name)


def Plot_ROC_Fn(label, distance, choice_phase, save_name):

    similarity_output = - distance

    # Calculating the ROC curve for the whole data.
    fpr, tpr, thresholds = metrics.roc_curve(label, similarity_output, pos_label=1)

    # for itr in range(k):

    # Calculating EER
    intersect_x = fpr[np.abs(fpr - (1 - tpr)).argmin(0)]
    EER = intersect_x
    # print("EER = ", float(("{0:.%ie}" % 1).format(intersect_x)))

    # AUC(area under the curve) calculation
    AUC = np.trapz(tpr, fpr)
    # print("AUC = ", float(("{0:.%ie}" % 1).format(AUC)))

    # Save .mat files
    sio.savemat('roc_data/fpr.mat', {'fpr': fpr})
    sio.savemat('roc_data/tpr.mat', {'tpr': tpr})
    sio.savemat('roc_data/label.mat', {'label': label})
    sio.savemat('roc_data/distance.mat', {'distance': distance})

    # Plot the ROC
    fig = plt.figure()
    ax = fig.gca()
    lines = plt.plot(fpr, tpr, label='ROC Curve')
    plt.setp(lines, linewidth=3, color='r')
    ax.set_xticks(np.arange(0, 1, 0.1))
    ax.set_yticks(np.arange(0, 1, 0.1))
    plt.title('ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    # Cutting the floating number
    AUC = '%.2f' % AUC
    EER = '%.2f' % EER

    # Setting text to plot
    plt.text(0.5, 0.5, 'AUC = ' + str(AUC), fontdict=None)
    plt.text(0.5, 0.4, 'EER = ' + str(EER), fontdict=None)
    plt.grid()
    plt.show()
    fig.savefig(choice_phase + '_' + save_name)


