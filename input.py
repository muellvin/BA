#input: b_sup, b_inf, h
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
    input_data = [b_sup, b_inf, h, M_Ed, V_Ed, T_Ed]
    return input_data