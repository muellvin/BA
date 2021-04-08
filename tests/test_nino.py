#This is a test script

import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA/ebplate')

import ebplate as ebp
stiffeners_ebp = []
stiffeners_ebp.append((600, 10, 6, 0.2))
#stiffeners_ebp.append((1200, 10, 6, 0.2))
phi_cr = ebp.ebplate(3000,2000,20,200,-200, stiffeners_ebp)
print(phi_cr)
#test
