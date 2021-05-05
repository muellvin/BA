import data
from optimizer import optimization_value

def into_collector(new_cs):
    optimization_value.set_value(cs)
    data.cs_collection.append(new_cs)



def get_best():
    if defaults.optimize_for_cost_only == True:
        forgot_default = False
        return get_best_cost()
    elif defaults.optimize_for_spec_ei == True:
        forgot_default = False
        return get_best_spec_ei()
    elif defaults.optimize_for_target_function == True:
        forgot_default = False
        return get_best_target_value()



def get_best_cost():
    best_cs = []
    if data.cs_collection == []:
        return best_cs
    else:
        for cs_fromall in data.cs_collection:
            add = False
            if best_cs == []:
                add = True
            else:
                for cs_frombest in best_cs:
                    if cs_fromall.cost < cs_frombest.cost:
                        add = True
                        best_cs.remove(cs_frombest)
                    elif cs_fromall.cost == cs_frombest.cost:
                        add = True
                    else:
                        add = False
            if add == True:
                best_cs.append(cs_fromall)
        return best_cs

def get_best_spec_ei():
    best_cs = []
    if data.cs_collection == []:
        return best_cs
    else:
        for cs_fromall in data.cs_collection:
            if abs(cs_from_all.ei / defaults.input_data.get("ei") - 1) < 0.05:
                add = False
                if best_cs == []:
                    add = True
                else:
                    for cs_frombest in best_cs:
                        if cs_fromall.cost < cs_frombest.cost:
                            add = True
                            best_cs.remove(cs_frombest)
                        elif cs_fromall.cost == cs_frombest.cost:
                            add = True
                        else:
                            add = False
                if add == True:
                    best_cs.append(cs_fromall)
        return best_cs

def get_best_target_value():
    best_cs = []
    if data.cs_collection == []:
        return best_cs
    else:
        for cs_fromall in data.cs_collection:
            add = False
            if best_cs == []:
                add = True
            else:
                for cs_frombest in best_cs:
                    if cs_fromall.target_value < cs_frombest.target_value:
                        add = True
                        best_cs.remove(cs_frombest)
                    elif cs_fromall.target_value == cs_frombest.target_value:
                        add = True
                    else:
                        add = False
            if add == True:
                best_cs.append(cs_fromall)
        return best_cs
