from classes import stiffener as st

def substantiate(propositions):
    #switch clause for respective plates
    for stiffener in propositions:
        if stiffener.pl_position == 1:
            pass
            #trackplate, this should be implemented differently, not here, just put here as a reminder
        elif stiffener.pl_position == 2:
            dimensions = find_dimensions_2(stiffener)
            #assign dimensions to proposition tbd
            #sidplate right side
        elif stiffener.pl_position == 3:
            dimensions = find_dimensions_3(stiffener)
            pass
            #bottom plate
        else:
            assert stiffener.pl_position == 4, "Plate not found."
            pass
            #left sideplate, should be symmetrical to right sideplate, this case can be dealt with quite easily

    #check if values are still set to default
    #idea: always keep one variable free and iterate through the others

def find_dimensions_2(stiffener):
    #initialize dimensions container
    #b_sup, b_inf, h, t, mass
    best = [0,0,0,0,0]
    #set maximum default values and step size for range
    b_inf_max = 250
    b_inf_step = 10
    b_sup_max = 250
    b_sup_step = 10
    h_max = 100
    h_step = 5
    t_range = [5,7,9,11,13,15,17,20]

    #set new default values, if corrections need to be made
    if stiffener.b_inf != 0:
        b_inf_max = stiffener.b_inf
        assert b_inf_max > b_inf_step, "Error, nothing could be found."

    if stiffener.b_sup != 0:
        b_sup_max = stiffener.b_sup
        assert b_sup_max > b_sup_step, "Error, nothing could be found."

    if stiffener.height != 0:
        h_max = stiffener.height
        assert h_max > h_step, "Error, nothing could be found"

    #iterate through all the possible solutions, in order to find viable ones

    #still make restriction for angle in for-loop and possibly other restrictions...
    best = [0,0,0,0,0]
    for b_sup in range(10, b_sup_max, b_sup_step):
        for h in range(10, h_max, h_step):
            for b_inf in range(10, b_inf_max, b_inf_step):
                for t in t_range:
                    I_a = st.get_i_along_stiffener(b_sup, b_inf, h, t)
                    if I_a > stiffener.i_along:
                        m = st.get_area_stiffener(b_sup, b_inf, h, t) #get_area to be implemented
                        if best[4] < m:
                            best = [b_sup, b_inf, h, t, m]

    print(best)
    return best

def find_dimensions_3():
    pass
