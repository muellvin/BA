import data
import defaults
from optimizer import optimization_value
from output import geometry_output

def into_collector(new_cs):
    optimization_value.set_value(new_cs)
    data.cs_collection.append(new_cs)

def print_best():
    i = 1
    for cs in get_best():
        cs.reset()
        name = "cs_"+str(i)
        geometry_output.print_cs_to_pdf(cs, input = True)

        cs = buckling_proof.buckling_proof(cs)

        ei = round(cs.get_ei() / 1000 / 1000 / 1000)
        interaction_2 = cs.interaction_2
        interaction_3 = cs.interaction_3
        interaction_4 = cs.interaction_4
        cost = optimization_value.cost(cs)
        line1 = "\n\nResults:"
        line2 = "\n   EI: "+str(ei)+"Nm^2"
        line3 = "\n   interaction side 2: "+str(interaction_2)
        line4 = "\n   interaction side 3: "+str(interaction_3)
        line5 = "\n   interaction side 4: "+str(interaction_4)
        line6 = "\n   cost: "+str(cost)+"CHF/m"
        string = line1 + line2 + line3 + line4 + line5 + line6
        printing.printing(string, terminal = True)

        geometry_output.print_cs_to_pdf(cs, input = False)
        printing.txt_to_pdf(name)


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
