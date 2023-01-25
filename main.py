from experiment.tilt_orient import *
import sys

# create the experiment with n_trial for each block
# different class for choices of IO methods
if not len(sys.argv) == 2:
    sub_val = str(input('Enter Unique Subject ID:'))
else:
    sub_val = str(sys.argv[1])

# start running the experiment
exp = OrientEncodeKeyboard(sub_val)

N_BLOCK = 4
N_RUN = 6

# Run 4 blocks with 6 runs within each block
for _ in range(N_BLOCK):

    for idx in range(N_RUN):
        if idx == 0:
            exp.start(wait_on_key=True)
        else:
            exp.start(wait_on_key=False)

        exp.run()
        exp.save_data()
        print('Finished 1 Run')