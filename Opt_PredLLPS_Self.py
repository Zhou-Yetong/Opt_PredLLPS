import numpy as np
import pandas as pd
import re
from utils.data_processing import load_data
from utils.Feature import load_multimodal_features
from tensorflow.keras import models
import argparse
import datetime
import warnings
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


seed = 7
np.random.seed(seed)

def test(args):
    inputfile = args.input_fasta_file
    id, seq = load_seqs(inputfile)

    # evolutionary information features
    test, labels = load_data(inputfile , 1)
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
    x1 = X_Test.reshape(X_Test.shape[0], X_Test.shape[1],X_Test.shape[2])

    # multimodal features
    data_list1 = load_multimodal_features(inputfile)
    x2_Test = np.array(data_list1)
    print(x2_Test.shape)
    x2 = x2_Test.reshape(x2_Test.shape[0], x2_Test.shape[1], 1)

    model=models.load_model("model/Opt_PredLLPS_Self.h5")
    y_predict = model.predict([x1,x2])
    y_pre_Self = []
    for i in y_predict:
        y_pre_Self.append(i[0])
    print(y_pre_Self)
    results = [id,seq, y_pre_Self]
    results = np.array(results)
    results = results.T
    results = pd.DataFrame(results, columns=['Description', 'Sequence',  'Opt_PredLLPS_Self score'])
    results.to_csv('Opt_PredLLPS_Self prediction results.csv', index=False, header=True, escapechar=',')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-input_fasta_file', type=str, default='test/Ind_Test_I/Ind_Test_I.fasta',help='Path of the input_fasta_file')

    args = parser.parse_args()
    start_time = datetime.datetime.now()
    print('******test******')
    test(args)
    end_time = datetime.datetime.now()
    print('End time(min):', (end_time - start_time).seconds / 60)

