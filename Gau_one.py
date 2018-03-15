import os
import re
from pandas import *


# This module defines an object to read a single Gaussian output file.
# The object can read the energies and setup a dataframe including the information of the 2 bead names, original energies in Hartree, deltaE in kcal/mol, etc.

class Gau_one(object):
    def __init__(self,filename):
        self.f= open(filename, 'r+')  # open source file 
        print('--'*20+'\n'+'open file: '+filename+'\n')
    #
    def searchenergies(self, keyword, distance, Nameof2beads, E_bead1= -305.1, E_bead2=-305.1):
        self.Ebd1 = E_bead1
        self.Ebd2 = E_bead2
        self.Name2bds = Nameof2beads
        self.dist = distance
        print('Name of the two beads: '+self.Name2bds)
        print('Energies of the two single beads: '+ str(self.Ebd1)+' , '+str(self.Ebd2) + ' in Hartrees \n')
        data = self.f.readlines()  #read all lines into local var
        # compile search engine
        # use regular expression to search the keyword pattern
        # the keyword is usually 'SCF Done' for the self consistent field calculations
        # in this case, the energy always follows the 'SCF Done' in the same line.
        # initialize the search engine:
        s = re.compile(keyword)
        #
        energies = []
        # scan through all lines
        for line in data:
            if s.search(line):
            # the 'if' pattern above chooses the lines containning energy infomation
                #
                engvalue = -float(re.search('(?<=-)(\d)+.(\d)+',line).group())
                # the line above is a new regular expression
                # to  match the pattern: [minus sign] + [some digits] + [.] + [some digits]
                # then, the pattern is converted into type float
                #
                energies.append(engvalue)    # make a list of wanted lines
        #
        # Create the date frame 
        self.df = DataFrame(energies,  columns = [self.Name2bds])
        self.df.insert(0,'Distance/A', self.dist)
        self.df.insert(2,'deltaE', self.df[self.Name2bds] - self.Ebd1-self.Ebd2) # calculate energy diffrence, insert column
        self.df.insert(3,'deltaE /(kcal/mol)', self.df['deltaE']*627.509)
        print( "energies captured: " + str(len(self.df)) + '\n')
        #
    def averageif(self,threshold):
        #
        self.thsd = threshold
        #
        self.selecteddf =  self.df.loc[self.df['deltaE /(kcal/mol)'] <= threshold]
        self.avgif =  self.selecteddf['deltaE /(kcal/mol)'].mean()
        #
        print("energies selected:"+str(len(self.selecteddf))+'\n')
        # Return the selected data(pointer), for convenience. 
        return self.selecteddf
        #
    #


