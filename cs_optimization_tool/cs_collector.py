from data_and_defaults import data
from data_and_defaults import defaults
from cs_optimization_tool import optimization_value

#function that adds a cross section to the cs_collection
def into_collector(new_cs):
    optimization_value.set_value(new_cs)
    data.cs_collection.append(new_cs)

def reset():
    data.cs_collection = []

#function that returns the optimal cross section
def get_best():
    if data.input_data.get("goal") == 0:
        forgot_default = False
        return get_best_cost()
    elif data.input_data.get("goal") == 1:
        forgot_default = False
        return get_best_spec_ei()
    else:
        assert data.input_data.get("goal") == 2, "Wrong Goal Input."
        forgot_default = False
        return get_best_ratio()


#function that returns the cheapest cross section that passed
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

#function that returns the cheapest cross section for a specific EI
def get_best_spec_ei():
    best_cs = []
    if data.cs_collection == []:
        return best_cs
    else:
        for cs_fromall in data.cs_collection:
            if abs(cs_from_all.ei / data.input_data.get("ei") - 1) < 0.05:
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

#function that returns the cross section with the best EI/Price-Ratio
def get_best_ratio():
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
                    if cs_fromall.ratio > cs_frombest.ratio:
                        add = True
                        best_cs.remove(cs_frombest)
                    elif cs_fromall.ratio == cs_frombest.ratio:
                        add = True
                    else:
                        add = False
            if add == True:
                best_cs.append(cs_fromall)
        return best_cs
