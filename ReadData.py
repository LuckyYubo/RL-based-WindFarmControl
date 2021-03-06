import numpy as np
import time

'''
This file is used to read data generated by FAST.Farm. Then the readed data will be transformed into samples to train the RL agent
'''

class Generate_Samples(object):
    def __init__(self, filename, num_col):
        '''
        filename: the name of file which saves the output of Fast.Farm
        num_col: the number of columes in the output file
        '''

        self.fn = filename
        self.num_col = num_col
    
    def ReadData(self, num_row_valid = 8):
        '''
        num_row_valid: the start of valid row number in the output file
        '''

        f = open(self.fn)
        line = f.readline()
        data = np.zeros(self.num_col)
        i = 1

        # from num_row_valid, read each line in the output file
        while line:
            if (i > num_row_valid):
                line_split = line.split()                        # split this line by " " 
                line_valid = list(map(float, line_split))        # transform char into float
                data = np.vstack((data, np.array(line_valid)))   # add this line to DATA
            
            i = i + 1
            line = f.readline()
        f.close
        self.data = data[1:, :]                                  # abandon the first empty line

    def Data2Samples(self, valid_col):

        # The sample structure is [s_t, a_t, r_t, s_t+1]
        # ValidCol = [6, 26, 27, 25, 24]

        num_valid_col = len(valid_col)
        num_samples = np.size(self.data, 0)
        self.samples = np.zeros((num_samples, num_valid_col))
        
        for i in range(num_valid_col):
            self.samples[:, i] = self.data[:, valid_col[i]]

        num_samples = num_samples - 1
        state_t1 = np.array(self.samples[1:, 0:3])
        # state_t1 = state_t1.reshape(num_samples, 1)
        self.samples = self.samples[0:num_samples, :]
        self.samples = np.hstack((self.samples, state_t1))
        
        return num_samples, self.samples