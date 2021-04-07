#buckling proof
import local_buckling
import column_buckling
import plate_global




"""4 Längspannung"""

"""4.4 Einzelfeldbeulen"""
#in a first step, the effective width of the plates are determined (rho of each plate)
#(iterative process): moving p1 and p2 of the
local_buckling.local_buckling(cs)

"""4.5 Längsausgesteifte Blechfelder"""
#plate behaviour with help of EB Plate
#column behaviour with 4.5
#interaction of plate and column in 4.5.4

#create a cs with all plates of this side
def global_buckling(cs, side):
    plate_glob = crosssection.crosssection()
    for line in cs.lines:
    if line.code.pl_position == side:
        plate_glob.addline(line)
    chi_c, sigma_cr_c = column_buckling.column_buckling(plate_glob)
    rho_p, sigma_cr_p = plate_global.plate_global(plate_glob)

    eta = sigma_cr_p/sigma_cr_c -1
    rho_c = (rho_p - chi_c) * eta * (2 - eta) + chi_c

    for line in cs.lines:
        if line.code.pl_position == side:
            line.rho_c = rho_c


"""3 Schubverzerrung"""
#3.2.1 mittragende Breite
#if one wants the deck to act plastically, we need to take an alpha_0 star
#that depends on the effective widths of the deck plate
#it is accounted for by reducing the thickness instead of the width (same result, easier calculation)



"""4.6 Nachweis"""
#gives us eta 1





"""5 Schubbeulen"""

"""5.5 Nachweis"""
#gives us eta 3





"""7 Interaktion"""
#7.1 Interaction between shear, bending moment and normal force with eta 1 and eta 3
