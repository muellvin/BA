#This is a test script

import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA/ebplate')

import initial_cs as ics
from proofs import global_buckling as globb
from proofs import local_buckling as locb
from output import geometry_output as go
import data
import deck
from classes import stiffener as st

data.input_data.update({"b_inf": 3000})
data.input_data.update({"b_sup": 4000})
data.input_data.update({"h": 1500})
data.input_data.update({"M_Ed": 50*10**9})
data.input_data.update({"Q_Ed": 1000})
data.input_data.update({"T_Ed": 1000})
data.input_data.update({"a": 1000})
data.input_data.update({"L_e": 1000})
data.input_data.update({"bending type": 1000})
data.input_data.update({"cs position": 1000})
initial_cs = ics.create_initial_cs(4000, 3000, 1500, 4, 4, 4)
deck_stiffeners = deck.deck(4000)
stiffened_cs = st.merge(initial_cs, deck_stiffeners)
reduced_cs = locb.local_buckling(stiffened_cs)
go.print_cs_red(reduced_cs)
final_cs = globb.global_buckling(reduced_cs)
go.print_cs(final_cs)
