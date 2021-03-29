import math
import initial_cs as ics
import optimizer
import deck
from classes import stiffener as stf
import data
from output import geometry_output as go

#run input script
from input import input

#create initial cross section
start_cs = ics.create_initial_cs(data.input_data[b_sup],data.input_data[b_inf],data.input_data[h])

#add deck stiffeners according to EN 3-2
deck_stiffeners = deck.deck(4000)
#no geomety check performed here, maybe this still needs to be implemented

#run optimizer
