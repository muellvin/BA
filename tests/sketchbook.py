import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

from optimizer import optimizer_nino
import data

data.input_data.update({"b_inf": 3000})
data.input_data.update({"b_sup": 4000})
data.input_data.update({"h": 1500})
data.input_data.update({"M_Ed": -70*10**8})
data.input_data.update({"V_Ed": 1000000})
data.input_data.update({"T_Ed": 100000000})
data.input_data.update({"a": 1000})
data.input_data.update({"L_e": 1000})
data.input_data.update({"t_deck": 16})
data.input_data.update({"bending type": "hogging bending"})
data.input_data.update({"cs position": 1000})
optimizer_nino.optimize()
