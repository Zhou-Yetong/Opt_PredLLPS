import re
import numpy as np
from utils.encoding_methods import pssm_encoding, hhm_encoding, cat



def load_seqs(fn, label):
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
                ids.append(t)
                t = 0
    if label == 1:
        labels = np.ones(len(ids))
    else:
        labels = np.zeros(len(ids))

    return ids, seqs, labels


def load_data(fasta_path, label):
    ids, seqs, labels = load_seqs(fasta_path, label)

    pssm_dir = '/'.join(fasta_path.split('/')[:-1]) + '/pssm/'
    pssm_encodings = pssm_encoding(ids, pssm_dir)

    hhm_dir = '/'.join(fasta_path.split('/')[:-1]) + '/hhm/'
    hhm_encodings = hhm_encoding(ids, hhm_dir)

    Xs = cat(hhm_encodings,pssm_encodings)
    data_list =Xs

    return data_list, labels

