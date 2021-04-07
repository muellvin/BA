from classes import crosssection


def column(plate_glob, side):
    #get the stiffeners
    stiffener_lines = []
    tpl_lines = []
    stiffeners = []
    for line in plate_glob.lines:
        if line.code.tpl_number == 0:
            stiffener_lines.append(line)
        elif line.code.tpl_number

    for i in range(int(len(stiffener_lines)/3)):
        stiffeners.append(crosssection.crosssection(0, 0, 0))
        for line in stiffener_lines:
            if line.code.st_number == i+1:
                stiffeners[i].lines.append(line)

    #EC 1993 1-5 (7) all combinations of stiffeners as a member have to be investigated
    #
    #according to the EC 1993 1-5 (1) the equivalent member can no longer be seen as supported on the sides
    #
    #according to A.2 (3) -> Illustration A.1
    #the contributing widths are the ones defined by local buckling
    #for both the stiffener and the neighbouring plates
