
import data


def sanity_check_everything():
    all_ok = True
    if check_input_data() == False:
        all_ok = False
    return all_ok


def check_input_data_complete():
    required_input_data = ["b_sup", "b_inf", "h", "M_Ed", "Q_Ed", "T_Ed", "a", "L_e", "bending type", "cs position"]
    #a is the length of a local buckling field, ie distance between stiffeners in longitudinal direction
    #L_e is the effective length of a continuous beam
    #bending type should either be "sagging bending" or "hogging bending"
    #cs position should either be "Cantilever", "end support" or "field"
    complete = True
    missing = []
    for input in required_input_data:
        if data.input_data.get(input) == None:
            complete = False
            missing.append(input)
    for input in missing:
        print(input)
    assert complete == True, "The input_data dictionary is incomplete!"
