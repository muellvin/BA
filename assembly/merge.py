
import math
import shapely
import random
import copy
from classes import point
from classes import line
from classes import crosssection
from classes import plate_code


#This functions merges a cross section and a list of stiffeners
def merge(initial_cs, stiffener_list):
    assert len(initial_cs.lines) == 4, "Merge does not accept crosssections with stiffeners"
    stiffeners1 = []
    stiffeners2 = []
    stiffeners3 = []
    stiffeners4 = []
    for stiffener in stiffener_list:
        pos = stiffener.lines[0].code.pl_position
        if pos == 1:
            stiffeners1.append(stiffener)
        elif pos == 2:
            stiffeners2.append(stiffener)
        elif pos == 3:
            stiffeners3.append(stiffener)
        elif pos == 4:
            stiffeners4.append(stiffener)
    #side 1
    new_tpl_lines_1 = []
    if stiffeners1 != []:
        stiffeners1 = sorted(stiffeners1, key = lambda st: st.lines[0].code.st_number)
        old_plate_1 = initial_cs.get_line(pl_position = 1, pl_type = 0)
        tpl_number_1_min = initial_cs.get_line(pl_position = 1, pl_type = 0).code.tpl_number
        initial_cs.lines.remove(initial_cs.get_line(pl_position = 1, pl_type = 0))

        t_1 = old_plate_1.t
        side = 1

        st_number_1_min = stiffeners1[0].lines[0].code.st_number
        st_number_1_max = st_number_1_min
        for stiffener in stiffeners1:
            this_st_number = stiffener.lines[0].code.st_number
            if this_st_number < st_number_1_min:
                st_number_1_min = this_st_number
            elif this_st_number > st_number_1_max:
                st_number_1_max = this_st_number

        i = st_number_1_min
        j = tpl_number_1_min
        next_tpl_a = None
        initial_point_1 = old_plate_1.a
        end_point_1 = old_plate_1.b

        while i <= st_number_1_max:

            new_plate_1_a = initial_point_1
            new_plate_1_b = copy.deepcopy(stiffeners1[i-st_number_1_min].get_line(pl_position = side, st_pl_position = 4).b)
            new_plate_2_a = copy.deepcopy(new_plate_1_b)
            new_plate_2_b = copy.deepcopy(stiffeners1[i-st_number_1_min].get_line(pl_position = side, st_pl_position = 2).a)
            next_tpl_a = copy.deepcopy(new_plate_2_b)
            code_1 = plate_code.plate_code(side, 0, j, 0, 0)
            code_2 = plate_code.plate_code(side, 0, j+1, i, 1)
            new_plate_1 = line.line(code_1, new_plate_1_a, new_plate_1_b, t_1)
            new_plate_2 = line.line(code_2, new_plate_2_a, new_plate_2_b, t_1)
            new_tpl_lines_1.append(new_plate_1)
            new_tpl_lines_1.append(new_plate_2)
            j += 2
            i += 1
            initial_point_1 = copy.deepcopy(new_plate_2_b)
        code_1 = plate_code.plate_code(side, 0, j, 0, 0)
        new_plate_1 = line.line(code_1, next_tpl_a, end_point_1, t_1)
        new_tpl_lines_1.append(new_plate_1)
        initial_cs.get_line(pl_position = 2, pl_type = 0).code.tpl_number = j+1
        initial_cs.get_line(pl_position = 3, pl_type = 0).code.tpl_number = j+2
        initial_cs.get_line(pl_position = 4, pl_type = 0).code.tpl_number = j+3

    #side 2
    new_tpl_lines_2 = []
    if stiffeners2 != []:
        stiffeners2 = sorted(stiffeners2, key = lambda st: st.lines[0].code.st_number)
        old_plate_2 = initial_cs.get_line(pl_position = 2, pl_type = 0)
        tpl_number_2_min = initial_cs.get_line(pl_position = 2, pl_type = 0).code.tpl_number
        initial_cs.lines.remove(initial_cs.get_line(pl_position = 2, pl_type = 0))
        t_2 = old_plate_2.t
        side = 2

        st_number_2_min = stiffeners2[0].lines[0].code.st_number
        st_number_2_max = st_number_2_min
        for stiffener in stiffeners2:
            this_st_number = stiffener.lines[0].code.st_number
            if this_st_number < st_number_2_min:
                st_number_2_min = this_st_number
            elif this_st_number > st_number_2_max:
                st_number_2_max = this_st_number

        i = st_number_2_min
        j = tpl_number_2_min
        next_tpl_a = None
        initial_point_2 = old_plate_2.a
        end_point_2 = old_plate_2.b

        while i <= st_number_2_max:
            new_plate_1_a = initial_point_2
            new_plate_1_b = copy.deepcopy(stiffeners2[i-st_number_2_min].get_line(pl_position = side, st_pl_position = 4).b)
            new_plate_2_a = copy.deepcopy(new_plate_1_b)
            new_plate_2_b = copy.deepcopy(stiffeners2[i-st_number_2_min].get_line(pl_position = side, st_pl_position = 2).a)
            next_tpl_a = copy.deepcopy(new_plate_2_b)
            code_1 = plate_code.plate_code(side, 0, j, 0, 0)
            code_2 = plate_code.plate_code(side, 0, j+1, i, 1)
            new_plate_1 = line.line(code_1, new_plate_1_a, new_plate_1_b, t_2)
            new_plate_2 = line.line(code_2, new_plate_2_a, new_plate_2_b, t_2)
            new_tpl_lines_2.append(new_plate_1)
            new_tpl_lines_2.append(new_plate_2)
            j += 2
            i += 1
            initial_point_2 = copy.deepcopy(new_plate_2_b)
        code_2 = plate_code.plate_code(side, 0, j, 0, 0)
        new_plate_2 = line.line(code_2, next_tpl_a, end_point_2, t_2)
        new_tpl_lines_2.append(new_plate_2)
        initial_cs.get_line(pl_position = 3, pl_type = 0).code.tpl_number = j+1
        initial_cs.get_line(pl_position = 4, pl_type = 0).code.tpl_number = j+2


    #side 3
    new_tpl_lines_3 = []
    if stiffeners3 != []:
        stiffeners3 = sorted(stiffeners3, key = lambda st: st.lines[0].code.st_number)
        old_plate_3 = initial_cs.get_line(pl_position = 3, pl_type = 0)
        tpl_number_3_min = initial_cs.get_line(pl_position = 3, pl_type = 0).code.tpl_number
        initial_cs.lines.remove(initial_cs.get_line(pl_position = 3, pl_type = 0))
        t_3 = old_plate_3.t
        side = 3

        st_number_3_min = stiffeners3[0].lines[0].code.st_number
        st_number_3_max = st_number_3_min
        for stiffener in stiffeners3:
            this_st_number = stiffener.lines[0].code.st_number
            if this_st_number < st_number_3_min:
                st_number_3_min = this_st_number
            elif this_st_number > st_number_3_max:
                st_number_3_max = this_st_number

        i = st_number_3_min
        j = tpl_number_3_min
        next_tpl_a = None
        initial_point_3 = old_plate_3.a
        end_point_3 = old_plate_3.b

        while i <= st_number_3_max:
            new_plate_1_a = initial_point_3
            new_plate_1_b = copy.deepcopy(stiffeners3[i-st_number_3_min].get_line(pl_position = side, st_pl_position = 4).b)
            new_plate_2_a = copy.deepcopy(new_plate_1_b)
            new_plate_2_b = copy.deepcopy(stiffeners3[i-st_number_3_min].get_line(pl_position = side, st_pl_position = 2).a)
            next_tpl_a = copy.deepcopy(new_plate_2_b)
            code_1 = plate_code.plate_code(side, 0, j, 0, 0)
            code_2 = plate_code.plate_code(side, 0, j+1, i, 1)
            new_plate_1 = line.line(code_1, new_plate_1_a, new_plate_1_b, t_3)
            new_plate_2 = line.line(code_2, new_plate_2_a, new_plate_2_b, t_3)
            new_tpl_lines_3.append(new_plate_1)
            new_tpl_lines_3.append(new_plate_2)
            j += 2
            i += 1
            initial_point_3 = copy.deepcopy(new_plate_2_b)
        code_3 = plate_code.plate_code(side, 0, j, 0, 0)
        new_plate_3 = line.line(code_3, next_tpl_a, end_point_3, t_3)
        new_tpl_lines_3.append(new_plate_3)
        initial_cs.get_line(pl_position = 4, pl_type = 0).code.tpl_number = j+1


    #side 4
    new_tpl_lines_4 = []
    if stiffeners4 != []:
        stiffeners4 = sorted(stiffeners4, key = lambda st: st.lines[0].code.st_number)
        old_plate_4 = initial_cs.get_line(pl_position = 4, pl_type = 0)
        tpl_number_4_min = initial_cs.get_line(pl_position = 4, pl_type = 0).code.tpl_number
        initial_cs.lines.remove(initial_cs.get_line(pl_position = 4, pl_type = 0))
        t_4 = old_plate_4.t
        side = 4

        st_number_4_min = stiffeners4[0].lines[0].code.st_number
        st_number_4_max = st_number_4_min
        for stiffener in stiffeners4:
            this_st_number = stiffener.lines[0].code.st_number
            if this_st_number < st_number_4_min:
                st_number_4_min = this_st_number
            elif this_st_number > st_number_4_max:
                st_number_4_max = this_st_number

        i = st_number_4_min
        j = tpl_number_4_min
        next_tpl_a = None
        initial_point_4 = old_plate_4.a
        end_point_4 = old_plate_4.b

        while i <= st_number_4_max:
            new_plate_1_a = initial_point_4
            new_plate_1_b = copy.deepcopy(stiffeners4[i-st_number_4_min].get_line(pl_position = side, st_pl_position = 4).b)
            new_plate_2_a = copy.deepcopy(new_plate_1_b)
            new_plate_2_b = copy.deepcopy(stiffeners4[i-st_number_4_min].get_line(pl_position = side, st_pl_position = 2).a)
            next_tpl_a = copy.deepcopy(new_plate_2_b)
            code_1 = plate_code.plate_code(side, 0, j, 0, 0)
            code_2 = plate_code.plate_code(side, 0, j+1, i, 1)
            new_plate_1 = line.line(code_1, new_plate_1_a, new_plate_1_b, t_4)
            new_plate_2 = line.line(code_2, new_plate_2_a, new_plate_2_b, t_4)
            new_tpl_lines_4.append(new_plate_1)
            new_tpl_lines_4.append(new_plate_2)
            j += 2
            i += 1
            initial_point_4 = copy.deepcopy(new_plate_2_b)
        code_4 = plate_code.plate_code(side, 0, j, 0, 0)
        new_plate_4 = line.line(code_4, next_tpl_a, end_point_4, t_4)
        new_tpl_lines_4.append(new_plate_4)

    for plate in new_tpl_lines_1:
        initial_cs.addline(plate)
    for plate in new_tpl_lines_2:
        initial_cs.addline(plate)
    for plate in new_tpl_lines_3:
        initial_cs.addline(plate)
    for plate in new_tpl_lines_4:
        initial_cs.addline(plate)

    for stiffener in stiffener_list:
        for i in range(len(stiffener.lines)):
            initial_cs.addline(stiffener.lines[i])

    return initial_cs
