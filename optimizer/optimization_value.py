import defaults
import data

def set_value(cs):
    if defaults.optimize_for_cost_only == True:
        cs.cost = cost(cs)
    elif defaults.optimize_for_spec_ei == True:
        cs.cost = cost(cs)
        cs.ei = ei(cs)
    elif defaults.optimize_for_target_function == True:
        cs.target_value = target_function(cs)



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
    cost = steel_mass * defaults.steel_cost + welding_length * defaults.welding_cost
    cost = round(cost)
    return cost

def ei(cs):
    ei = cs.get_i_y_red()*data.constants.get("E")
    return ei

def target_function(cs):
    target_value = defaults.weight_cost*cost(cs) + defaults.weight_ei*ei(cs)
    return target_value
