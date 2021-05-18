import os
import sys

def ebplate(b, h, t, sigma_a, sigma_b, stiffeners_ebp):
    #write the input for ebplate to ebplate.EBP
    os.remove("ebplate\plate.EBP")
    file = open("ebplate\plate.EBP", 'a+', encoding ='cp1252')
    file.write("	EBPlate - v2.01 \n")
    file.write("Société       # \n")
    file.write("Affaire       # \n")
    file.write("Référence     # \n")
    file.write("Utilisateur   # \n")
    file.write("Commentaire   # \n")
    file.write("#PLATE \n")
    file.write("   Width           " + str(b/10) + " cm \n")
    file.write("   Height          " + str(h/10) + " cm \n")
    file.write("   Thickness         " + str(t/10) + " cm \n")
    file.write("   Module Young    210000.000 MPa \n")
    file.write("   Poisson Coefficient         0.300 \n")
    file.write("   Boundary Conditions \n")
    file.write("      Bord 1 0 \n")
    file.write("      Bord 2 0 \n")
    file.write("      Bord 3 0 \n")
    file.write("      Bord 4 0 \n")
    file.close()
    if len(stiffeners_ebp) > 0 :
        file = open("ebplate\plate.EBP", 'a+', encoding ='cp1252')
        file.write("#STIFFENING \n")
        file.write("   Orthotropic Plate =  1 \n")
        file.write("   Coefficients d'orthotropie : \n")
        file.write("      Direction X : Beta =  0.000 \n")
        file.write("                     Eta =  -1.000 \n")
        file.write("        Smearing : No \n")
        file.write("      Direction Y : Beta =  0.000 \n")
        file.write("                     Eta =  0.000 \n")
        file.write("        Smearing : No \n")
        file.write("   Referentiel 2 \n")
        file.write("   Nombre de raidisseurs  " + str(len(stiffeners_ebp)) + " \n")
        file.close()
        for i in range(len(stiffeners_ebp)):
            file = open("ebplate\plate.EBP", 'a+', encoding ='cp1252')
            file.write("   - Raidisseur n° " + str(i+1) + " Active=1 \n")
            file.write("      Orientation = 0 \n")
            file.write("      Position    = " + str(stiffeners_ebp[i][0]/10) + " \n")
            file.write("      Gamma       = " + str(stiffeners_ebp[i][1]) + " \n")
            file.write("      Teta        = " + str(stiffeners_ebp[i][2]) + " \n")
            file.write("      Delta       = " + str(stiffeners_ebp[i][3]) + " \n")
            file.write("      Dimension 1 = 0 \n")
            file.write("      Type        = 0 \n")
            file.write("      Dimension 2 = 0 \n")
            file.write("      Dimension 3 = 0 \n")
            file.write("      Dimension 4 = 0 \n")
            file.close()
    else:
        file = open("ebplate\plate.EBP", 'a+', encoding ='cp1252')
        file.write("#STIFFENING \n")
        file.write("   Orthotropic Plate =  0 \n")
        file.write("   Referentiel 2 \n")
        file.write("   Nombre de raidisseurs  " + str(len(stiffeners_ebp)) + " \n")
        file.close()
    file = open("ebplate\plate.EBP", 'a+', encoding ='cp1252')
    file.write("#STRESSES \n")
    file.write(" Longitudinal stresses : User's data No \n")
    file.write(" Analytical Longitudinal stresses \n")
    file.write("  Imposed values : No \n")
    file.write("   Longitudinal Stress Top Left                " + str(sigma_b) + " MPa \n")
    file.write("   Longitudinal Stress Bottom Left             " + str(sigma_a) + " MPa \n")
    file.write("   Longitudinal Stress Top Right               " + str(sigma_b) + " MPa \n")
    file.write("   Longitudinal Stress Bottom Right            " + str(sigma_a) + " MPa \n")
    file.write(" Transverse stresses : User's data No \n")
    file.write(" Analytical Transverse stresses \n")
    file.write("  Imposed values : No \n")
    file.write("   Transverse stress Top                         0.000 MPa \n")
    file.write("   Transverse stress Bottom                      0.000 MPa \n")
    file.write("   Patch Load Stress Bottom                      0.000 MPa \n")
    file.write("   Patch Load Stress Top                         0.000 MPa \n")
    file.write("   Patch Load Width Top                          0.000 cm \n")
    file.write("   Patch Load Width Bottom                       0.000 cm \n")
    file.write("   Local longitudinal stresses under patch load : No \n")
    file.write("   Local shear stresses under patch load : Yes \n")
    file.write("   W Top                      -1.000 \n")
    file.write("   W Bot                      -1.000 \n")
    file.write("   Shear distribution  1 \n")
    file.write("Shear stresses : User's data No \n")
    file.write("Analytical Shear stresses \n")
    file.write("  Imposed values : No \n")
    file.write("   Shear stress                                 0.000 MPa \n")
    file.write("#PARAMETERS \n")
    file.write("   Complexity : 1 \n")
    file.write("   Effective width parameter :  10.000")
    file.close()
    #run ebplate calculation from your own directory
    #os.system(r'"C:\Program Files (x86)\EBPlate\EBPlate.exe" /BATCH C:\Users\Nino\Google Drive\Studium\FS 2021\Bachelorarbeit\BA\ebplate\plate.EBP')
    os.system(r'"C:\Program Files (x86)\EBPlate\EBPlate.exe" /BATCH C:\Users\Vinzenz Müller\Dropbox\ETH\6. Semester\BA\ebplate\plate.EBP')

    #get phi_cr from the ebplate.EBR
    result_file = open('ebplate\plate.EBR', 'r', encoding = 'cp1252')
    results_text = result_file.readlines()
    phi_cr_line = results_text[1]
    phi_cr = float(phi_cr_line[7:])

    return phi_cr

def ebplate_shear(b, h, t, tau, stiffeners_ebp):
        #write the input for ebplate to ebplate.EBP
        os.remove("ebplate\plate.EBP")
        file = open("ebplate\plate.EBP", 'a+', encoding ='cp1252')
        file.write("	EBPlate - v2.01 \n")
        file.write("Société       # \n")
        file.write("Affaire       # \n")
        file.write("Référence     # \n")
        file.write("Utilisateur   # \n")
        file.write("Commentaire   # \n")
        file.write("#PLATE \n")
        file.write("   Width           " + str(b/10) + " cm \n")
        file.write("   Height          " + str(h/10) + " cm \n")
        file.write("   Thickness         " + str(t/10) + " cm \n")
        file.write("   Module Young    210000.000 MPa \n")
        file.write("   Poisson Coefficient         0.300 \n")
        file.write("   Boundary Conditions \n")
        file.write("      Bord 1 0 \n")
        file.write("      Bord 2 0 \n")
        file.write("      Bord 3 0 \n")
        file.write("      Bord 4 0 \n")
        file.write("#STIFFENING \n")
        file.write("   Orthotropic Plate =  0 \n")
        file.write("   Referentiel 2 \n")
        file.write("   Nombre de raidisseurs  " + str(len(stiffeners_ebp)) + " \n")
        file.close()
        for i in range(len(stiffeners_ebp)):
            file = open("ebplate\plate.EBP", 'a+', encoding ='cp1252')
            file.write("   - Raidisseur n° " + str(i+1) + " Active=1 \n")
            file.write("      Orientation = 0 \n")
            file.write("      Position    = " + str(stiffeners_ebp[i][0]/10) + " \n")
            file.write("      Gamma       = 0 \n")
            file.write("      Teta        = 0 \n")
            file.write("      Delta       = 0 \n")
            file.write("      Type        = 3 \n")
            file.write("      Dimension 1 = " + str(stiffeners_ebp[i][1]/10) + " \n")
            file.write("      Dimension 2 = " + str(stiffeners_ebp[i][2]/10) + " \n")
            file.write("      Dimension 3 = " + str(stiffeners_ebp[i][3]/10) + " \n")
            file.write("      Dimension 4 = " + str(stiffeners_ebp[i][4]/10) + " \n")
            file.close()
        file = open("ebplate\plate.EBP", 'a+', encoding ='cp1252')
        file.write("#STRESSES \n")
        file.write(" Longitudinal stresses : User's data No \n")
        file.write(" Analytical Longitudinal stresses \n")
        file.write("  Imposed values : No \n")
        file.write("   Longitudinal Stress Top Left                0.000 MPa \n")
        file.write("   Longitudinal Stress Bottom Left             0.000 MPa \n")
        file.write("   Longitudinal Stress Top Right               0.000 MPa \n")
        file.write("   Longitudinal Stress Bottom Right            0.000 MPa \n")
        file.write(" Transverse stresses : User's data No \n")
        file.write(" Analytical Transverse stresses \n")
        file.write("  Imposed values : No \n")
        file.write("   Transverse stress Top                         0.000 MPa \n")
        file.write("   Transverse stress Bottom                      0.000 MPa \n")
        file.write("   Patch Load Stress Bottom                      0.000 MPa \n")
        file.write("   Patch Load Stress Top                         0.000 MPa \n")
        file.write("   Patch Load Width Top                          0.000 cm \n")
        file.write("   Patch Load Width Bottom                       0.000 cm \n")
        file.write("   Local longitudinal stresses under patch load : No \n")
        file.write("   Local shear stresses under patch load : Yes \n")
        file.write("   W Top                      -1.000 \n")
        file.write("   W Bot                      -1.000 \n")
        file.write("   Shear distribution  1 \n")
        file.write("Shear stresses : User's data No \n")
        file.write("Analytical Shear stresses \n")
        file.write("  Imposed values : No \n")
        file.write("   Shear stress                                 " + str(tau) + " MPa \n")
        file.write("#PARAMETERS \n")
        file.write("   Complexity : 1 \n")
        file.write("   Effective width parameter :  10.000")
        file.close()
        #run ebplate calculation from your own directory
        #os.system(r'"C:\Program Files (x86)\EBPlate\EBPlate.exe" /BATCH C:\Users\Nino\Google Drive\Studium\FS 2021\Bachelorarbeit\BA\ebplate\plate.EBP')
        os.system(r'"C:\Program Files (x86)\EBPlate\EBPlate.exe" /BATCH C:\Users\Vinzenz Müller\Dropbox\ETH\6. Semester\BA\ebplate\plate.EBP')

        #get phi_cr from the ebplate.EBR
        result_file = open('ebplate\plate.EBR', 'r', encoding = 'cp1252')
        results_text = result_file.readlines()
        phi_cr_line = results_text[1]
        phi_cr = float(phi_cr_line[7:])

        return phi_cr
