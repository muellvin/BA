#This is a test script

import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA/ebplate')

import ebplate as ebp
phi_cr = ebp.ebplate(3000,2000,20,200,-200)
print(phi_cr)
#test
