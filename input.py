#input from user prompt
def userprompt():
    print('Value of b_sup? [mm]')
    b_sup = input()
    print('Value of b_inf? [mm]')
    b_inf = input()
    print('Value of h? [mm]')
    h = input()
    print('Value of M_Ed? [kNm]')
    M_Ed= input()
    print('Value of V_Ed? [kN]')
    V_Ed = input()
    print('Value of T_Ed? [kNm]')
    T_Ed = input()
    geometry_data = [b_sup, b_inf, h]
    load_data = [M_Ed, V_Ed, T_Ed]
    return geometry_data, load_data

#set of standard test cases
#containers still need to be filled with reasonable values

def standard_test_case(test_number):
    assert input > 0 and input < 4
    if test_number == 1:
        geometry_data = [1,1,1]
        load_data = [1,1,1]
        return geometry_data, load_data
    elif test_number == 2:
        geometry_data = [1,1,1]
        load_data = [1,1,1]
        return geometry_data, load_data
    else
        geometry_data = [1,1,1]
        load_data = [1,1,1]
        return geometry_data, load_data
