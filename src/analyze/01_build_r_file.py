#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
:author: Maximilian Golla
:contact: golla@cispa.de
:version: 0.0.4, 2023-12-17
'''

import sys
import re
from collections import OrderedDict

def read_file(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as inputfile:
        inputfile.readline() # skip header
        for line in inputfile:
            try:
                line = line.rstrip('\r\n')
                data.append(line)
            except Exception as e:
                sys.stderr.write(f"Error: {e} - {line}\n")
    return data

def _prepare_dict(strength, weight, withcount):
    pw_re = re.compile(r'^\s*[0-9]*\s')
    occ_re = re.compile(r'^\s*[0-9]*')

    output = OrderedDict()
    for i in range(0, len(strength)):
        p = withcount[i].replace(pw_re.findall(withcount[i])[0], '')
        s = float(strength[i])
        w = float(weight[i])
        c = float(occ_re.findall(withcount[i])[0].replace(' ', ''))
        output[i] = {'password': p, 'strength': s, 'weight': w, 'count': c}
    return output

def _add_meter(output, meter_name, meter_result_file):
    meter_data = read_file(meter_result_file)
    i = 0
    for entry in output:
        output[entry][meter_name] = float(meter_data[i])
        i += 1
    return output

def build_online(dataset_name):
    strength = read_file(f"../datasets/online/{dataset_name}/1_{dataset_name}.online.strength")
    weight = read_file(f"../datasets/online/{dataset_name}/2_{dataset_name}.online.weight")
    withcount = read_file(f"../datasets/online/{dataset_name}/3_{dataset_name}.online.withcount")
    output = _prepare_dict(strength, weight, withcount)
    output = _add_meter(output, "zxcvbn_guess_number", f"../crawl/01_zxcvbn/0_{dataset_name}.online.pw_guess_number_result.txt")
    output = _add_meter(output, "zxcvbn_score", f"../crawl/01_zxcvbn/0_{dataset_name}.online.pw_score_result.txt")
    return output

def build_offline(dataset_name):
    strength = read_file(f"../datasets/offline/{dataset_name}/1_{dataset_name}.offline.strength")
    weight = read_file(f"../datasets/offline/{dataset_name}/2_{dataset_name}.offline.weight")
    withcount = read_file(f"../datasets/offline/{dataset_name}/3_{dataset_name}.offline.withcount")
    output = _prepare_dict(strength, weight, withcount)
    output = _add_meter(output, "zxcvbn_guess_number", f"../crawl/01_zxcvbn/0_{dataset_name}.offline.pw_guess_number_result.txt")
    output = _add_meter(output, "zxcvbn_score", f"../crawl/01_zxcvbn/0_{dataset_name}.offline.pw_score_result.txt")
    return output

def write_result(filename, result):
    with open(filename, 'w', encoding='utf-8') as outputfile:
        # Write header
        header = list(result[0].keys())
        outputfile.write("{}\n".format("\t".join(header)))
        # Write data
        line_number = 1
        for entry in result:
            outputfile.write("{}\n".format("\t".join([str(i) for i in result[entry].values()])))
            line_number += 1

def main():
    datasets = ['linkedin', '000webhost', 'rockyou']
    try:
        for dataset_name in datasets:
            result = build_online(dataset_name)
            write_result(f"result_{dataset_name}_online.csv", result)
            result = build_offline(dataset_name)
            write_result(f"result_{dataset_name}_offline.csv", result)
    except Exception as e:
        sys.stderr.write(f"Error: {e} - {dataset_name}\n")

if __name__ == '__main__':
    main()
