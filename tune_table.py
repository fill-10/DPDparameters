from bdpair_reg import bdpair_reg
from Gau_one import Gau_one
import pandas as pd
import scipy as sp

class tune_table(object):
    def __init__(self, pandasfiledataframe):
        self.pfdf = pandasfiledataframe
        self.FittingAll = pd.DataFrame(columns = ['aij_int', 'bij_int'])
    #
    def gettable(self, ifsaveunselected = False):
        for Row  in self.pfdf.iterrows():
            C_series  = Row[1].dropna()
            print("sssssssssssssssss")

            print(C_series)
            print("sssssssssssssssss")
            # iterrows() returns a tuple: (name, series), where name is the index of the row, equivalent to series.name.
            # Use .iloc to choose the wanted data column(s).
            # For each pair, define the object from bdpair_reg
            # It will calculate the average if, plot the regression, and save the xlsx file for the bead pair.
            bdp_reg = bdpair_reg(C_series.name, C_series.iloc[3:].values, C_series.iloc[3:].index, C_series.iloc[0] ,C_series.iloc[1])
            #
            # Make dataframes (all and below threshold) for the bead pair. The second argument controls the output of the discarded conformations which are above the energy threshold.
            bdp_reg.mk2df(C_series.iloc[2], ifsaveunselected)
            #
            # Call plotavg() to perform the regression and plot the fitted curve.
            bdp_reg.plotavg()
            #
            # After all, save the fitted parameters, as long as the file list, for a single bead pair.
            bdp_reg.writexlsx(C_series.name+'_avg_reg.xlsx')
            # Single run done in the loop of bead pairs.
            #
            # Save the parameters
            self.FittingAll = self.FittingAll.append(    pd.DataFrame(    [[bdp_reg.slope, bdp_reg.intercept]] , index =  [bdp_reg.nm] ,columns = self.FittingAll.columns.values   )    )
            print(self.FittingAll)
            
            # The function gettable() is done!

    def tunevalues(self, R_critical, tunefactor):
        self.factor = tunefactor
        self.rc  = R_critical
        self.FittingAll['aij_int_astr'] = self.FittingAll['aij_int']/self.factor/self.rc/self.rc
        self.FittingAll['bij_int_astr'] = self.FittingAll['bij_int']/self.factor
        self.FittingAll['aij_ex'] = self.FittingAll['aij_int_astr'] + self.FittingAll['bij_int_astr']
        self.FittingAll['aij'] = self.FittingAll['aij_ex'] +25.0
    def writefittingallxlsx(self, xlsxfilename):
        self.Fitxlsxfn = xlsxfilename
        writer = pd.ExcelWriter(self.Fitxlsxfn)
        self.FittingAll.to_excel(writer)
        writer.save()



# example to run:

if __name__ == '__main__':
    
    ft = pd.DataFrame([[-305.113287901, -305.113287901, 120.0, '../OH-OH_550.log','../OH-OH_600.log', '../OH-OH_650.log','../OH-OH_700.log']] , index = ['OH-OH'], columns = ['Ebd1_Hartree','Ebd2_Hartree','Ethreshold_kcal/mol', 5.5, 6., 6.5, 7.])
    
    #print(ft)

    tt = tune_table(ft)
    tt.gettable(True)
    tt.tunevalues(7.11, 2.856)
    print( tt.FittingAll )
    tt.writefittingallxlsx('FittingAll.xlsx')
