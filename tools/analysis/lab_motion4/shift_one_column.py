##
## compatible with old scipy version

import csv
import numpy as np
from scipy.spatial.transform import Rotation as R

import sys
import argparse


def dataFromCSV(data_path):
    with open(data_path, 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        data = list(reader)

        data = np.array(data)
        data[data == ''] = '0'
        data = data.astype(np.float64)
        data[:,0] = data[:,0]

    return data

## main function

data_file = sys.argv[1]

## input data
data =  dataFromCSV(data_file)
data[:,0] = data[:,0]-780

# output file
output_file = './shift/'+data_file
print('output_file: {} '.format(output_file))
np.savetxt(output_file, data, delimiter=' ', fmt=('%10.9f', '%2.6f', '%2.6f', '%2.6f', '%2.6f', '%2.6f', '%2.6f', '%2.6f'))
