import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')

import data

data.input_data.update({"b_inf": 1000})
data.input_data.update({"b_sup": 1000})
data.input_data.update({"h": 1000})
data.input_data.update({"M_Ed": 1000})
data.input_data.update({"Q_Ed": 1000})
data.input_data.update({"T_Ed": 1000})
data.input_data.update({"a": 1000})
data.input_data.update({"L_e": 1000})
data.input_data.update({"bending type": 1000})
data.input_data.update({"cs position": 1000})





data.check_input_data_complete()
