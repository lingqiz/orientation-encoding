import os, sys, numpy as np
from numpy import genfromtxt
from scipy.io import savemat

# set up the path
input_args = sys.argv
input_args.pop(0)
sub_name = input_args[0]

home = os.path.expanduser('~')
base = os.path.join(home, 'Data', 'fMRI',
                    sub_name, 'attenRT')

# get all csv files, sort by modificaiton time
files = [os.path.join(base, fl) for fl in os.listdir(base)]
files.sort(key=lambda x: os.path.getmtime(x))

# read in the time
all_time = []
for fl in files:
    # print out file name to make sure
    # the sequence is ordered correctly
    print(fl)
    time_data = genfromtxt(fl, delimiter=',')
    all_time.append(time_data)

all_time = np.array(all_time, dtype='object')
savemat(os.path.join(base, 'atten_time.mat'),
        {'time': all_time})