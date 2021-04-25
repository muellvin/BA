import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')
#sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

import initial_cs
from proofs import local_buckling
from proofs import column_buckling
from proofs import global_buckling
from output import geometry_output
from classes import stiffener
from classes import stiffeners_proposition
from classes import proposed_stiffener
from classes import crosssection
import deck
import data
import defaults

defaults.set_cs_defaults()
defaults.set_forces_defaults()


cs = initial_cs.create_initial_cs(data.input_data.get("b_sup"), data.input_data.get("b_inf"), data.input_data.get("h"), 20, 20, 20)
geometry_output.print_cs_red(cs)
deck_stiffeners = deck.deck(data.input_data.get("b_sup"))
cs = stiffener.merge(cs, deck_stiffeners)
geometry_output.print_cs_red(cs)

prop_list = stiffeners_proposition.stiffeners_proposition()
#propose stiffeners, mimicking input from optimizer

prop_1 = proposed_stiffener.proposed_stiffener(2, 1, 0.5, 10**7)
prop_list.add(prop_1)

#prop_2 = ps.proposed_stiffener(2, 2, 0.3, 10**7)
#prop_list.add(prop_2)
prop_3 = proposed_stiffener.proposed_stiffener(3, 2, -0.7, 10**7)
prop_list.add(prop_3)
prop_4 = proposed_stiffener.proposed_stiffener(3, 3, 0.7, 10**7)
prop_list.add(prop_4)
#prop_5 = ps.proposed_stiffener(4, 5, 0.3, 10**7)
#prop_list.add(prop_5)
prop_5 = proposed_stiffener.proposed_stiffener(4, 4, 0.5, 10**7)
prop_list.add(prop_5)




cs = stiffener.add_stiffener_set(cs, prop_list)
geometry_output.print_cs_red(cs)


cs = local_buckling.local_buckling(cs)

print(cs)
cs = global_buckling.global_buckling(cs)

print("area_tot: ", cs.get_area_tot())
print("area_red: ", cs.get_area_red())
print("center_y_tot: ", cs.get_center_y_tot())
print("center_y_red: ", cs.get_center_y_red())
print("center_z_tot: ", cs.get_center_z_tot())
print("center_z_red: ", cs.get_center_z_red())
print("i_y_tot: ", cs.get_i_y_tot())
print("i_y_red: ", cs.get_i_y_red())
print("i_z_tot: ", cs.get_i_z_tot())
print("i_z_red: ", cs.get_i_z_red())



geometry_output.print_cs_red(cs)
