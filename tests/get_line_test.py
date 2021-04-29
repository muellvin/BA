import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')
#sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

import initial_cs
from proofs import local_buckling
from proofs import column_buckling
from output import geometry_output
from classes import stiffener
from classes import stiffeners_proposition
from classes import proposed_stiffener
from classes import crosssection
from classes import merge
import deck
import data

b_sup = 3000
b_inf = 2000
h = 1500
M_Ed = -100000000
data.input_data["M_Ed"] = M_Ed
data.input_data["h"] = h
data.input_data["b_inf"] = b_inf
data.input_data["b_sup"] = b_sup

print(data.input_data)
print(data.constants)


cs = initial_cs.create_initial_cs(b_sup, b_inf, h, 20, 20, 20)
geometry_output.print_cs_red(cs)
#deck_stiffeners = deck.deck(b_sup)
#cs = merge.merge(cs, deck_stiffeners)

#prop_list = stiffeners_proposition.stiffeners_proposition()
#
#prop_1 = proposed_stiffener.proposed_stiffener(2, 1, 0.5, 10**7)
#prop_list.add(prop_1)
#prop_3 = proposed_stiffener.proposed_stiffener(3, 2, -0.7, 10**7)
#prop_list.add(prop_3)
#prop_4 = proposed_stiffener.proposed_stiffener(3, 3, 0.7, 10**7)
#prop_list.add(prop_4)
#prop_5 = proposed_stiffener.proposed_stiffener(4, 4, 0.5, 10**7)
#prop_list.add(prop_5)

line = cs.get_line(pl_position = 1)

new_cs = crosssection.crosssection (0,0,0)
geometry_output.print_cs_red(new_cs)
