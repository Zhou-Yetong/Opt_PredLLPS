import numpy as np
import csv
import math
import re
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from propy.AAComposition import CalculateAAComposition



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
                ids.append(t)
                t = 0
    return seqs


AA_array = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
            'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']


kd = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5,
      "C": 2.5, "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2,
      "I": 4.5,
      "L": 3.8, "K": -3.9,
      "M": 1.9,
      "F": 2.8, "P": -1.6, "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3,
      "V": 4.2}

def hydrophobicity(seq):
    sequence = ProteinAnalysis(seq)
    HB = 0
    for k in range(0, len(AA_array)):
        HB = HB + sequence.count_amino_acids()[AA_array[k]] * kd[AA_array[k]]
    #HB = HB / len(seq)
    return HB


def Shannon_entropy(seq):
    sequence = ProteinAnalysis(seq)
    entropy = 0
    for k in range(0, len(AA_array)):
        if sequence.get_amino_acids_percent()[AA_array[k]] == 0:
            entropy = entropy + 0
        else:
            entropy = entropy - math.log2(sequence.get_amino_acids_percent()[AA_array[k]]) * \
                      sequence.get_amino_acids_percent()[AA_array[k]]
    return entropy


def load_feature(fasta_path):
    hhm_dir = '/'.join(fasta_path.split('/')[:-1])+'/'
    with open(hhm_dir + fasta_path.split('/')[-1][:-6] +'.csv', 'r') as f:
        data = list(csv.reader(f))
        data=data[1:]
        feature=[]
        for i in data:
            a=i[2:7]
            feature.append(a)
    return feature

def cat(*args):
    """
    :param args: feature matrices
    """
    res = args[0]
    for matrix in args[1:]:
        for i in range(len(matrix)):
            res[i] = np.hstack((res[i], matrix[i]))
    return res


def load_multimodal_features(fasta_path):
    seqs = load_seqs(fasta_path)
    feature = load_feature(fasta_path)
    Feature = []
    for i in seqs:
        aac = CalculateAAComposition(i)
        aac = list(aac.values())
        HB = hydrophobicity(i)
        aac.append(HB)
        entropy = Shannon_entropy(i)
        aac.append(entropy)
        Feature.append(aac)
    Feature = cat(Feature, feature)
    return Feature

