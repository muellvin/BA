import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')

import initial_cs
from proofs import local_buckling
from output import geometry_output
import data

b_sup = 4000
b_inf = 2000
h = 1500
M_Ed = 1000
data.input_data["M_Ed"] = M_Ed
data.input_data["h"] = h
data.input_data["b_inf"] = b_inf
data.input_data["b_sup"] = b_sup

cs = initial_cs.create_initial_cs(b_sup, b_inf, h, 20, 20, 20)





cs = local_buckling.local_buckling(cs)

output.geometry_output.print_cs(cs)
