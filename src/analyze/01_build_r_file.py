#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
:author: Maximilian Golla
:contact: maximilian.golla@rub.de
:version: 0.0.2, 2019-04-24
'''

import sys, re
from collections import OrderedDict

def read_file(filename):
    data = []
    with open(filename, 'r') as inputfile:
        inputfile.readline() # skip header
        for line in inputfile:
            try:
                line = line.rstrip('\r\n')
                data.append(line)
            except Exception as e:
                sys.stderr.write("Error: {} - {}\n".format(e, line))
    return data

def _prepare_dict(strength, weight, withcount):
    pw_re = re.compile('^\s*[0-9]*\s')
    occ_re = re.compile('^\s*[0-9]*')

    output = OrderedDict()
    for i in xrange(0, len(strength)):
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

def build_online():
    strength = read_file("../datasets/online/1_linkedin.online.strength")
    weight = read_file("../datasets/online/2_linkedin.online.weight")
    withcount = read_file("../datasets/online/3_linkedin.online.withcount")
    output = _prepare_dict(strength, weight, withcount)
    output = _add_meter(output, "zxcvbn_guess_number", "../crawl/01_zxcvbn/0_linkedin.online.pw_guess_number_result.txt")
    output = _add_meter(output, "zxcvbn_score", "../crawl/01_zxcvbn/0_linkedin.online.pw_score_result.txt")
    return output

def build_offline():
    strength = read_file("../datasets/offline/1_linkedin.offline.strength")
    weight = read_file("../datasets/offline/2_linkedin.offline.weight")
    withcount = read_file("../datasets/offline/3_linkedin.offline.withcount")
    output = _prepare_dict(strength, weight, withcount)
    output = _add_meter(output, "zxcvbn_guess_number", "../crawl/01_zxcvbn/0_linkedin.offline.pw_guess_number_result.txt")
    output = _add_meter(output, "zxcvbn_score", "../crawl/01_zxcvbn/0_linkedin.offline.pw_score_result.txt")
    return output

def write_result(filename, result):
    with open(filename, 'w') as outputfile:
        # Write header
        header = []
        for title in result.itervalues().next():
            header.append(title)
        outputfile.write("{}\n".format("\t".join(header)))
        # Write data
        line_number = 1
        for entry in result:
            outputfile.write("{}\n".format("\t".join([str(i) for i in result[entry].values()])))
            line_number += 1

def main():
    result = build_online()
    write_result("result_online.csv", result)
    result = build_offline()
    write_result("result_offline.csv", result)

if __name__ == '__main__':
    main()
