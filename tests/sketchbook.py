import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

from proofs import shear_lag

beta = shear_lag.beta_from_kappa(0.6)
print(beta)
