import os
import numpy as np

def load_pssm(query, pssm_path):
    if pssm_path[-1] != '/': pssm_path += '/'
    with open(pssm_path + query + '.pssm', 'r') as f:
        lines = f.readlines()
        res = []
        for line in lines[3:]:
            line = line.strip()
            lst = line.split(' ')
            while '' in lst:
                lst.remove('')
            if len(lst) == 0:
                break
            r = lst[2:22]
            r = [int(x) for x in r]
            res.append(r)
    return res


def load_hhm(query, hhm_path):
    if hhm_path[-1] != '/': hhm_path += '/'
    with open(hhm_path + query + '.hhm', 'r') as f:
        lines = f.readlines()
        res = []
        tag = 0
        for line in lines:
            line = line.strip()
            if line == '#':
                tag = 1
                continue
            if tag != 0 and tag < 5:
                tag += 1
                continue
            if tag >= 5:
                line = line.replace('*', '0')
                lst = line.split('\t')
                if len(lst) >= 20:
                    tmp0 = [int(lst[0].split(' ')[-1])]
                    tmp1 = list(map(int, lst[1:20]))
                    tmp0.extend(tmp1)
                    normed = [i if i == 0 else 2 ** (-0.001 * i) for i in tmp0]
                    res.append(normed)
    return res


def pssm_encoding(ids, pssm_dir):

    if pssm_dir[-1] != '/': pssm_dir += '/'
    pssm_fs = os.listdir(pssm_dir + 'output/')

    res = []
    for id in ids:
        name = id
        if id[0] == '>': name = id[1:]
        if name + '.pssm' in pssm_fs:
            # psiblast
            tmp = load_pssm(name, pssm_dir + 'output/')
            res.append(np.array(tmp))
    return res


def hhm_encoding(ids, hhm_dir):

    if hhm_dir[-1] != '/': hhm_dir += '/'
    hhm_fs = os.listdir(hhm_dir + 'output/')
    res = []
    for id in ids:
        name = id
        if id[0] == '>': name = id[1:]
        if name + '.hhm' in hhm_fs:
            tmp = load_hhm(name, hhm_dir + 'output/')
            res.append(np.array(tmp))
    return res

def cat(*args):
    res = args[0]
    for matrix in args[1:]:
        for i in range(len(matrix)):
            res[i] = np.hstack((res[i], matrix[i]))
    return res



