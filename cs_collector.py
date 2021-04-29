import data

def into_collector(new_cs):
    data.cs_collection.append(new_cs)

def get_best():
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
