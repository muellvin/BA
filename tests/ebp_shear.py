import sys
import os

#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
#sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')

from ebplate import ebplate

stiffener_list =[(1000, 150, 300, 200, 12)]
ebplate.ebplate_shear(4000, 4000, 12, 30, stiffener_list)
