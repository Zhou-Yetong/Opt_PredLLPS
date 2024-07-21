import numpy as np
import pandas as pd
from utils.data_processing import load_data
from utils.Feature import load_multimodal_features
from tensorflow.keras import models
import argparse
import datetime
import warnings
import pickle
import csv
import re
warnings.filterwarnings("ignore")
def load_seqs(fn):
    ids = []
    seqs = []
    t = 0
    pattern = re.compile('[^ARNDCQEGHILKMFPSTWYV]')
    with open(fn, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line[0] == '>':
                t = line.replace('|', '_')
            elif len(pattern.findall(line)) == 0:
                seqs.append(line)
                ids.append(t[1:])
                t = 0
    return ids,seqs

def load_data_Physicochemical(fasta_path):
    Feature_dir = '/'.join(fasta_path.split('/')[:-1]) + '/'
    with open(Feature_dir +'35+hydrophobicity+Omega'+ '.csv', 'r') as f:
        data = list(csv.reader(f))
        data = data[1:]
        Feature = []
        for i in data:
            a = i[1:]
            Feature.append(a)
    return Feature


# # 独立测试
def test(args):
    inputfile = args.input_fasta_file
    id, seq = load_seqs(inputfile)

#the first task model
    #evolutionary information features
    data, labels = load_data(inputfile, 1)
    a = [0 for col in range(40)]
    Test = []
    for i in range(len(labels)):
        x = data[i]
        x = x.tolist()
        b=[a]* (5000- len(x))
        c=np.vstack((x, b))
        c = np.array(c)
        Test.append(c)
    X_Test = np.array(Test)
    print(X_Test.shape)
    x1 = X_Test.reshape(X_Test.shape[0], X_Test.shape[1],X_Test.shape[2])

    # multimodal features
    data2 = load_multimodal_features(inputfile)
    x2_Test = np.array(data2)
    print(x2_Test.shape)
    x2 = x2_Test.reshape(x2_Test.shape[0], x2_Test.shape[1], 1)

    model1=models.load_model("model/the first task model.h5")
    y_pre = model1.predict([x1,x2])
    y_pre_LLPS=[]
    for i in y_pre:
        y_pre_LLPS.append(i[0])
    print(y_pre_LLPS)


#the second task model
    #Physicochemical_features
    data3 = load_data_Physicochemical(inputfile)
    x3_Test = np.array(data3, dtype=object)
    print(x3_Test.shape)
    model2 = pickle.load(open("model/the second task model.dat", "rb"))
    y_pre_self_part = model2.predict(x3_Test)
    print(y_pre_self_part)

    results = [id,seq, y_pre_LLPS,  y_pre_self_part]
    results = np.array(results)
    results = results.T
    results = pd.DataFrame(results, columns=['Description', 'Sequence', 'the first task score', 'the second task score'])
    results.to_csv('Opt_PredLLPS predict results.csv', index=False, header=True, escapechar=',')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-input_fasta_file', type=str, default='test/9 proteins/test.fasta',help='Path of the input_fasta_file')

    args = parser.parse_args()
    start_time = datetime.datetime.now()
    print('******test******')
    test(args)
    end_time = datetime.datetime.now()
    print('End time(min):', (end_time - start_time).seconds / 60)

