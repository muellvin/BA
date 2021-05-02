import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

from optimizer import optimizer_nino
from proofs import global_plate_buckling
from classes import crosssection
import data
import initial_cs as ics
import deck
from output import geometry_output
from classes import stiffener
from classes import merge
from proofs import resistance_to_shear
import math

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


initial_cs = ics.create_initial_cs(4000, 3000, 2000, 7, 7, 7)

st_list_deck = deck.deck(4000)

s = len(st_list_deck)

stiffener_1 = stiffener.create_stiffener_global(3, s+1, -1000, 2000, math.pi, 300, 200, 200, 15)
stiffener_2 = stiffener.create_stiffener_global(3, s+2, 1000, 2000, math.pi, 300, 200, 200, 15)


st_list_rest = [stiffener_1, stiffener_2]

st_list = st_list_deck + st_list_rest

print(len(st_list))

final_cs = merge.merge(initial_cs, st_list)
geometry_output.print_cs(final_cs)

plate_glob = final_cs.get_stiffened_plate(side = 3)
geometry_output.print_cs(plate_glob)

resistance_to_shear.resistance_to_shear(plate_glob, data.input_data.get("V_Ed"))
