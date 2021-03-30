import math
import initial_cs as ics
import optimizer as opt
import deck
from classes import stiffener as stf
import data
from output import geometry_output as go

#run input script
from input import input

#add deck stiffeners according to EN 3-2
deck_stiffeners = deck.deck(data.input_data[b_sup])

#call optimizer
#optimizer returns a list of cross sections that pass the buckling proof
base_cs_collection = opt.step_1()
preselected_cs_collection = opt.step_2(base_cs_collection)
end_cs_collection = opt.step_3(preselected_cs_collection)

#call goal function to assess the various cross sections
#returns "the best" cross section

#output
