#This is a test script

import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA/ebplate')

from proofs import resistance_to_shear as rts
from classes import crosssection as cs
from classes import stiffener as st
import deck 
import data
import initial_cs as ics


data.input_data.update({"b_inf": 3000})
data.input_data.update({"b_sup": 4000})
data.input_data.update({"h": 1500})
data.input_data.update({"M_Ed": 50*10**9})
data.input_data.update({"Q_Ed": 100*10**3})
data.input_data.update({"T_Ed": 30*10**6})
data.input_data.update({"a": 1000})
data.input_data.update({"L_e": 1000})
data.input_data.update({"bending type": 1000})
data.input_data.update({"cs position": 1000})

initial_cs = ics.create_initial_cs(4000, 3000, 1500, 4, 4, 4)
deck_stiffeners = deck.deck(4000)
stiffened_cs = st.merge(initial_cs, deck_stiffeners)
plate_glob = cs.crosssection(0,0,0)
for line in stiffened_cs.lines:
    if line.code.pl_position == 1:
        plate_glob.addline(line)

eta_3 = rts.resistance_to_shear(stiffened_cs, plate_glob)
print("eta3 = " + str(eta_3))
