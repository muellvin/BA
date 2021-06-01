from data_and_defaults import defaults
from data_and_defaults import data

#function that calculates Cost/EI and stores it in the cross section object
def set_value(cs):
    cs.cost = cost(cs)
    cs.ei = ei(cs)
    cs.ratio = ratio(cs)


#function that returns the cost of a given cross section
def cost(cs):
    #calculate material per meter length of bridge
    density = 7850 #density of steel
    steel_mass = cs.get_area_tot() / 1000**2 * density

    #calculate length of welds per meter length of bridge
    num_stiffeners = 0
    for plate in cs.lines:
        if plate.code.st_number > num_stiffeners:
            num_stiffeners = plate.code.st_number
    welding_length = 4 + num_stiffeners * 2

    #calculate etsimated costs
    cost = steel_mass * defaults.data.input_data.get("steel_cost") + welding_length * defaults.data.input_data.get("welding_cost")
    cost = round(cost)
    return cost

#function that returns EI of a cross section
def ei(cs):
    ei = cs.get_ei()
    return ei

#function that returns the EI/Cost-Ratio of a cross section
def ratio(cs):
    target_value =  ei(cs)/cost(cs)
    return target_value
