import csv
import numpy as np
from scipy.spatial.transform import Rotation as R

import sys
import argparse

time_index_map = {
## handheld-lab-simple
'lab-simple1': 5645.179542390,
'lab-simple2': 5725.990606451,
'lab-simple3': 5800.002496175,
## handheld-lab-motion
'lab-motion1': 858.828367331,
'lab-motion2': 1179.124723715,
'lab-motion3': 620.74158628,
'lab-motion4': 795.027770684,
'lab-motion5': 55500.154868292,
'lab-motion6': 55631.844341273,
## handheld-lab-light
'lab-light1': 1430.872305079,
'lab-light2': 1569.199532825,
'lab-light3': 348.185657436,
'lab-light4': 25509.090028725,
'lab-light5': 1564.450962713,
'lab-light6': 1694.879961643,
## handheld-lab-dynamic
'lab-dynamic1': 1015.839053138,
'lab-dynamic2': 1382.506229709,
'lab-dynamic3': 1945.370618162,
'lab-dynamic4': 12815.547334773,
'lab-dynamic5': 13102.889270907,
## handheld-corridor
'corridor1':1429.843360791,
'corridor2':2567.387245158,
'corridor3':1120.039553804,
'corridor4':1388.710462629,
## handheld-hall
'hall1':2809.832627107,
'hall2':3416.940431843,
'hall3':226.740069808,
## robot-manual
'lab-manual1':193443.642084968,
'lab-manual2':193614.659717371,
'lab-manual3':193804.507317469,
## robot-bumper
'lab-bumper1':3348.721497606,
'lab-bumper2':3624.756204693,
'lab-bumper3':24305.238540249,
'lab-bumper4':24456.282658849,
'lab-bumper5':24861.813846655,
## robot-corridor-manual
'corridor-manual1': 768.813970368,
'corridor-manual2': 3604.818084375,
## robot-corridor-bumper
'corridor-bumper1': 4589.798765979,
'corridor-bumper2': 6756.646370621
}

def dataFromCSV(data_path):
    with open(data_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)

        data = np.array(data)
        data[data == ''] = '0'
        data = data.astype(np.float64)
        data[:,0] = data[:,0]/1e9

    return data

def find_nearest(array, v):
    array  = np.asarray(array)
    idx = (np.abs(array-v)).argmin()
    return idx


## main function

if len(sys.argv) < 3:
    print ("usage: python process_result.py [data].csv [data_sequence_name]")
    exit(0)

data_file = sys.argv[1]
data_name = sys.argv[2]

if data_name not in time_index_map:
    print("data_name: % not in time_index_map".format(data_name))
    exit(0)

## input data
data = dataFromCSV(data_file)

## find out the zero time for synchronization
time_zero = time_index_map[data_name]
start_idx = find_nearest(data[0,:], float(time_zero))

## extract the synchronized data
data = data[start_idx:-1, 0:8]

# convert to TUM: 'timestamp tx ty tz qx qy qz qw'
# vins's output :w x y z'
quatXYZ = np.copy(data[:,5:8])
quatW = np.copy(data[:,4])
data[:,4:7]= quatXYZ
data[:,7]= quatW

# set the start point as original point of the world coordinate system
Tow = np.matrix(np.identity( 4 ))
t = data[0,1:4]
Tow[0:3,3] = t.reshape((3, 1))
r = R.from_quat(data[0,4:8])

Tow[0:3,0:3] = r.as_dcm();
Tow = np.linalg.inv(Tow)

for i in range(data.shape[0]):
    Twi = np.matrix(np.identity(4))
    Twi[0:3,3] = data[i,1:4].reshape((3,1))
    Twi[0:3,0:3] = R.from_quat(data[i,4:8]).as_dcm();

    Toi = Tow * Twi;
    data[i,1:4] = Toi[0:3,3].reshape(3);
    data[i,4:8] = R.from_dcm(Toi[0:3,0:3]).as_quat()

# output file
output_file = data_file[:-4]+'_tum.csv'
print('output_file: {} '.format(output_file))
np.savetxt(output_file, data, delimiter=' ', fmt=('%10.9f', '%2.6f', '%2.6f', '%2.6f', '%2.6f', '%2.6f', '%2.6f', '%2.6f'))
