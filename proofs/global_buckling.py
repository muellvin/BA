def global_buckling(cs):
    cs = global_buckling(cs, 2)
    cs = global_buckling(cs, 3)
    cs = global_buckling(cs, 4)
    return cs

#create a cs with all plates of this side
def reduction_global_buckling(cs, side):
    plate_glob = crosssection.crosssection()
    for line in cs.lines:
    if line.code.pl_position == side:
        plate_glob.addline(line)

    chi_c, sigma_cr_c = column.column(plate_glob)
    rho_p, sigma_cr_p = plate_global.plate_global(cs, plate_glob)


    eta = sigma_cr_p/sigma_cr_c -1
    rho_c = (rho_p - chi_c) * eta * (2 - eta) + chi_c

    for line in cs.lines:
        if line.code.pl_position == side:
            line.rho_c = rho_c

    return cs
