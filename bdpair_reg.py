import os
from Gau_one import Gau_one
import numpy as np
import pandas as pd

###----------------------------------------------###
### use these lines when running on qchem2, etc. ###
### matplotlib chooses Xwindow backend by default.
### You need to set matplotlib to not use Xwindos
### backend.
###----------------------------------------------###
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


import statsmodels.api as sm
import scipy as sp

class bdpair_reg(object):
    def __init__(self, nameof2beads, filename_list, distance_list, E_bead1, E_bead2):
        self.nm = nameof2beads
        self.E_bd1 = E_bead1
        self.E_bd2 = E_bead2
        self.dfavg = pd.DataFrame(filename_list, columns = ['GauFile'])
        self.dfavg['Distance/A'] = distance_list
        # Create an empty dataframe for all data points
        self.dframe = pd.DataFrame(columns = ['Distance/A', self.nm, 'deltaE', 'deltaE /(kcal/mol)'])
        # Dataframe for averaged energies (small table)
        self.dfavg['deltaE /(kcal/mol)'] = np.nan
    #
    # Make the wholelist
    #
    def mk2df(self, v_threshold, saveunselected = False):
        self.thsd = v_threshold

        # Deal with each Gaussian file
        indx = 0 # temp index for distance list
        for f in self.dfavg['GauFile']:
            SG = Gau_one(f)
            SG.searchenergies('SCF Done',self.dfavg['Distance/A'][indx], self.nm, self.E_bd1, self.E_bd2)
            self.dframe = self.dframe.append(SG.averageif(self.thsd))
            self.dfavg['deltaE /(kcal/mol)'][indx] = SG.avgif
            indx += 1
        #
            if saveunselected:
                unsel = SG.df.loc[SG.df['deltaE /(kcal/mol)'] > SG.thsd]
                if len(unsel):
                    unsel.to_excel(f+'_unselected.xlsx')

        self.dframe['rij'] = self.dframe['Distance/A'] / 7.11 # rc = 7.11A
        self.dframe['Xrij'] = 0.5* (1- self.dframe['rij'] )**2
        self.dframe['Uij'] = self.dframe['deltaE /(kcal/mol)'] / 0.5924  # 0.5924 kcal/mol = 1 dpd energy
        self.dfavg['rij'] = self.dfavg['Distance/A'] / 7.11
        self.dfavg['Xrij'] =  0.5 * (1 - self.dfavg['rij'])**2
        self.dfavg['Uij'] =  self.dfavg['deltaE /(kcal/mol)'] / 0.5924


    ###########################################
    # The damned statsmodels is hard to use for the whole dataframe.
    # There is always the error when calling rsquared or summary().
    # It might be a bug... 
    # But statsmodels works good with the small-sized 'averaged dataframe', which does not have the duplicated x_value. 
    def sm_regrss_all(self):
        return 
        #smresult = sm.OLS(self.dframe['Uij'], sm.add_constant(b.dframe['Xrij'])).fit()

    def sp_regrss_all(self):
        # Instead of statsmodels, use scipy.stats instead.  
        slope, intercept, r_value, p_value, std_error= sp.stats.linregress(self.dframe['Xrij'], self.dframe['Uij'])
        return slope, intercept, r_value**2
    #
    # Here includes the statsmodels linear regression for 'averaged frame'
    def sm_regrss_avg(self):
        rslt = sm.OLS(self.dfavg['Uij'], sm.add_constant(self.dfavg['Xrij'])).fit()
        return rslt.params, rslt.rsquared

    def sp_regrss_avg(self):
        #tmp_X = self.dfavg['Xrij']
        #tmp_Y = self.dfavg['Uij'].astype(float).values
        #print(tmp_Y)

        ###-------------------------------------------###
        ### In the line below, use .astype(float).values
        ### to convert pandas series into np.array.
        ### if not, there might be data type errors 
        ### in some versions of scipy.
        ###-------------------------------------------###
        slope, intercept, r_value, p_value, std_error= sp.stats.linregress(self.dfavg['Xrij'].astype(float).values, self.dfavg['Uij'].astype(float).values)
        # in python3 or above, return a tuple is the safest way.
        return (slope, intercept, r_value**2)
    
    def plotall(self):
        pass

    def plotavg(self):
        self.slope, self.intercept, self.rsquare =  self.sp_regrss_avg()
        #print( self.slope, self.intercept)
        xx = sp.linspace(   self.dfavg['Xrij'].min() - 0.25 * (self.dfavg['Xrij'].mean() -  self.dfavg['Xrij'].min()), \
                            self.dfavg['Xrij'].max() + 0.25 * (self.dfavg['Xrij'].max() -  self.dfavg['Xrij'].mean()), \
                            50)
        yy = xx*self.slope + self.intercept
        fig, ax = plt.subplots(figsize = (8, 6))
        ax.plot(self.dfavg['Xrij'], self.dfavg['Uij'], 'o', label = 'Uij')
        ax.plot(xx, yy, 'r--', label = 'fitted' )
        ax.legend(loc = 'best')
        fig.savefig(self.nm+'_reg_avg.png')


    def writexlsx(self, filename):
        self.xlsxfn = filename
        writer = pd.ExcelWriter(self.xlsxfn)
        self.dfavg.to_excel(writer)
        self.df_fitted = pd.DataFrame([self.slope , self.intercept, self.rsquare], index = ['slope', 'intercept', 'rsquared_avg'])
        self.df_fitted.to_excel(writer, startcol = 10, startrow = 1, header = False)
        writer.save()
    #
