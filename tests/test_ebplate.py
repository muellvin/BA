import sys
import os
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA/ebplate')

os.system(r'"C:\Program Files (x86)\EBPlate\EBPlate.exe" /BATCH C:\Users\Nino\Google Drive\Studium\FS 2021\Bachelorarbeit\BA\ebplate\plate-original.EBP')

#get phi_cr from the ebplate.EBR
result_file = open('ebplate\plate-original.EBR', 'r')
results_text = result_file.readlines()
phi_cr_line = results_text[1]
phi_cr = float(phi_cr_line[7:])

print(phi_cr)
