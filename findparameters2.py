from tune_table import tune_table
import pandas as pd



InputTab = pd.read_excel('./Input_Filelist.xlsx','Sheet1')

print('Input Files: ')
print(InputTab)
print('#'*40+'\n')

ft = tune_table(InputTab)

ft.gettable()

# If some existing aij_int and bij_int need to be added, use ft.FittingAll.append() here.

ft.tunevalues(7.11, 2.311)
ft.writefittingallxlsx('FittingaAll_test.xlsx')

#################################
#
#################################




#####################################
# Test bdpair_reg class
####################################
#
# from bdpair_reg import bdpair_reg
# b = bdpair_reg('OH-OH',['OH-OH_550.log','OH-OH_600.log','OH-OH_650.log','OH-OH_700.log'],[5.5,6.0,6.5,7.0], -305.113287901, -305.113287901)
# b.mk2df(100.0, True)
#
#
#
# print('\n\n'+'*'*20+'\n')
#
# b.plotavg()
#
# b.writexlsx(b.nm+'_avg_out.xlsx')
#
#########################################
