from proofs import buckling_proof
import cs_collector
import data
from classes import proposed_stiffener


#an optimizer that puts the stiffeners in place, such that the single plates inbetween each have the same total pressure
def opt_eqpressure(cs):
    t_values = [5, 10, 20]
    n_st_side_max = 8
    n_st_bottom_max = 10

    for t_side in t_values:
        set_t_side(cs,t_side)

        for t_bottom in t_values:
            set_t_bottom(cs, t_bottom)

            stop_side = False

            n_st_side = 0
            while n_st_side <= n_st_side_max and stop_side == False:
                set_stiffeners_side(cs, n_st_side)

                n_st_bottom = 0
                while n_st_bottom <= n_st_bottom_max and stop_bottom == False:

                    set_stiffeners_bottom(cs, n_st_bottom)
                    cs = buckling_proof.buckling_proof(cs)

                    if passed == True:
                        cs_collector.into_collector(cs)
                        stop = True
    return cs

def set_t_side(cs, t_side):
    for plate in cs.lines:
        if plate.code.pl_type == 0 and (plate.code.pl_position == 2 or plate.code.pl_position == 4):
            plate.t = t_side
    return cs

def set_t_bottom(cs, t_bottom):
    for plate in cs.lines:
        if plate.code.pl_type == 0 and plate.code.pl_position == 3:
            plate.t = t_side
    return cs

def set_stiffeners_side(cs, amount):
    if amount == 0:
        return cs
    else:
        pass

def set_stiffeners_bottom(cs, amount):
    if amount == 0:
        return cs
    else:
        cs_b_inf = data.input_data.get("b_inf")
        b_st_sup = data.input_data.get("b_inf")/(2*amount + 1)
