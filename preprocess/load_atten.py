import os, sys

input_args = sys.argv
input_args.pop(0)
sub_name = input_args[0]

home = os.path.expanduser('~')
base = os.path.join(home, 'Data', 'fMRI',
                    sub_name, 'attenRT')

files = [os.path.join(base, fl) for fl in os.listdir(base)]
files.sort(key=lambda x: os.path.getmtime(x))

for fl in files:
    print(fl)