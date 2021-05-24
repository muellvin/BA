from data_and_defaults import defaults
from data_and_defaults import data

def set_value(cs):
    if data.input_data.get("goal") == 0:
        cs.cost = cost(cs)
    elif data.input_data.get("goal") == 1:
        cs.cost = cost(cs)
        cs.ei = ei(cs)
    else:
        assert data.input_data.get("goal") == 2, "Wrong Goal Input."
        cs.ratio = ratio(cs)



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

def ei(cs):
    ei = cs.get_ei()
    return ei

def ratio(cs):
    target_value =  ei(cs)/cost(cs)
    return target_value
