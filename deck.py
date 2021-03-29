
def trackplate():
    #returns the dimensions for a track plate stiffener
    #thickness of plate itself should somewhere be set to 16mm! --> tbd

    #set maximum default values and step size for range
    b_inf_max_geo = 500
    b_inf_step = 10
    h_max_geo = 200
    h_step = 5
    #must be >6mm according to EC 3-2
    t_range = [7,9,11,13,15,17,20]

    #b_sup, b_inf, h, t, mass
    best = [0,0,0,0,10**8]

    #iterate through all the possible solutions, in order to find viable ones
    assert b_sup_max_geo > 50
    for t in t_range:
        b_sup = min(25*t, 300)
        b_inf_min = 10*math.floor(max(0,b_sup - 2*h)/10)
        b_inf_max = 10*math.floor(min(b_sup - 2*h/math.tan(math.pi/3), b_inf_max_geo)/10)
        if b_inf_min < b_inf_max:
            for b_inf in range(b_inf_min, b_inf_max, b_inf_step):
                for h in range(30, h_max, h_step):
                    I_a = st.get_i_along_stiffener(b_sup, b_inf, h, t)
                    if I_a > stiffener.i_along:
                        m = st.get_area_stiffener(b_sup, b_inf, h, t) #get_area to be implemented
                        if m < best[4]:
                            best = [b_sup, b_inf, h, t, m]

    b_sup = best[0]
    b_inf = best[1]
    h = best[2]
    t = best[3]
    return b_sup, b_inf, h, t


def min_inertial_mom():
    #returns the minimal required inertial moment of the track plate according to EC-3 2
    #This inertial momenent is calculated with the track plate
    #Lower Inertial moments for stiffeners in the corners should be considered
    #Minimal value of track plate thickness should be considered somewhere
    I = 15*10**6
    return I
