#einfach ein skript
import data

print('Value of b_sup? [mm]')
b_sup = input()
data.input_data.update({"b_sup": b_sup})

print('Value of b_inf? [mm]')
b_inf = input()
data.input_data.update({"b_inf": b_inf})

print('Value of h? [mm]')
h = input()
data.input_data.update({"h": h})

print('Value of M_Ed? [kNm]')
M_Ed= input()
data.input_data.update({"M_Ed": M_Ed})

print('Value of V_Ed? [kN]')
V_Ed = input()
data.input_data.update({"V_Ed": V_Ed})

print('Value of T_Ed? [kNm]')
T_Ed = input()
data.input_data.update({"T_Ed": T_Ed})
