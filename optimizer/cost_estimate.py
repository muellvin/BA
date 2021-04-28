import defaults

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
