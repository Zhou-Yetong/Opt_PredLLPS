import numpy as np
from utils.data_processing import load_data
from utils.Feature import load_multimodal_features
from tensorflow.keras import models
import argparse
import math
from sklearn.metrics import roc_auc_score
import datetime
import warnings
warnings.filterwarnings("ignore")


def Twoclassfy_evalu(y_test, y_predict):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    FP_index = []
    FN_index = []
    for i in range(len(y_test)):
        if y_predict[i] > 0.5 and y_test[i] == 1:
            TP += 1
        if y_predict[i] > 0.5 and y_test[i] == 0:
            FP += 1
            FP_index.append(i)
        if y_predict[i] < 0.5 and y_test[i] == 1:
            FN += 1
            FN_index.append(i)
        if y_predict[i] < 0.5 and y_test[i] == 0:
            TN += 1
    Sn = TP / (TP + FN)
    Sp = TN / (FP + TN)
    Pre = TP / (TP + FP)
    MCC = (TP * TN - FP * FN) / math.sqrt((TN + FN) * (FP + TN) * (TP + FN) * (TP + FP))
    Acc = (TP + TN) / (TP + FP + TN + FN)
    F1 = (2 * Pre * Sn) / (Pre + Sn)
    auc = roc_auc_score(y_test, y_predict)
    return Sn, Sp, Acc, MCC,auc,Pre,F1,TP,TN,FP,FN

seed = 7
np.random.seed(seed)

def test(args):
    # evolutionary information features
    positive = args.pos_test
    test, labels = load_data(positive, 1)
    negative = args.neg_test
    neg_test = load_data(negative, 0)
    test.extend(neg_test[0])
    labels = np.concatenate((labels, neg_test[1]), axis=0)
    a = [0 for col in range(40)]
    Test = []
    for i in range(len(labels)):
        x = test[i]
        x = x.tolist()
        b=[a]* (5000- len(x))
        c=np.vstack((x, b))
        c = np.array(c)
        Test.append(c)
    X_Test = np.array(Test)
    print(X_Test.shape)
    y = np.array(labels)
    x1 = X_Test.reshape(X_Test.shape[0], X_Test.shape[1],X_Test.shape[2])

    # multimodal features
    data_list1 = load_multimodal_features(positive)
    neg_data1 = load_multimodal_features(negative)
    data_list1.extend(neg_data1)
    x2_Test = np.array(data_list1)
    print(x2_Test.shape)
    x2 = x2_Test.reshape(x2_Test.shape[0], x2_Test.shape[1], 1)

    model=models.load_model("model/Opt_PredLLPS_Self.h5")
    y_predict = model.predict([x1,x2])
    (SN, SP, ACC, MCC, AUC,Pre,F1,TP,TN,FP,FN) = Twoclassfy_evalu(y, y_predict)

    print('TP:', TP)
    print('FN:', FN)
    print('TN:', TN)
    print('FP:', FP)
    print('SN:', '%.2f'%SN)
    print('SP:', '%.2f'%SP)
    print('ACC:', '%.2f'%ACC)
    print('MCC:', '%.2f'%MCC)
    print('Pre', '%.2f'%Pre)
    print('F1_score', '%.2f'%F1)
    print('AUC:', '%.2f'%AUC)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
#test/Ind_Test_I\P/Ind_Test_I_P.fasta   SaPS_test\P/SaPS_P.fasta
    parser.add_argument('-pos_test', type=str, default='test/SaPS_test\P/SaPS_P.fasta',
                        help='Path of the positive training dataset')
#test/Ind_Test_I/N/Ind_Test_I_N.fasta   SaPS_test/N/SaPS_N.fasta
    parser.add_argument('-neg_test', type=str, default='test/SaPS_test/N/SaPS_N.fasta',
                        help='Path of the negative training dataset')
    args = parser.parse_args()
    start_time = datetime.datetime.now()
    print('******test******')
    test(args)
    end_time = datetime.datetime.now()
    print('End time(min):', (end_time - start_time).seconds / 60)

