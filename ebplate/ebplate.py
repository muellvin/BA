import os

def ebplate(b, h, t, sigma_a, sigma_b, stiffeners_ebp):
    #write the input for ebplate to ebplate.EBP
    input_file = open('ebplate\plate.EBP', 'w')
    preamble = ["EBPlate - v2.01 \n",
                "Firm          # \n",\
                "Contract      # \n",\
                "Item          # \n",\
                "Users         # \n",\
                "Commentary    # \n"]
    input_file.writelines(preamble)
    plate = ["#PLATE \n",\
             "   Width           " + str(b/10) + " cm \n",\
             "   Height          " + str(h/10) + " cm \n",\
             "   Thickness       " + str(t/10) + " cm \n",\
             "   Young Modulus    210000.000 MPa \n",\
             "   Poisson Ratio        0.300 \n",\
             "   Boundary Conditions \n",\
             "      Edge 1 0 \n",\
             "      Edge 2 0 \n",\
             "      Edge 3 0 \n",\
             "      Edge 4 0 \n"]
    input_file.writelines(plate)
    stiffening_preamble = ["#STIFFENING \n",\
                  "   Orthotropic Plate =  1 \n",\
                  "   Orthotropic coefficients \n",\
                  "   X Direction : Beta = 0 \n",\
                  "                 Eta = -1 \n",\
                  "   Smearing : No \n",\
                  "   Y Direction : Beta = 0 \n",\
                  "                 Eta = 0 \n",\
                  "   Referential 1 \n",\
                  "   Number of stiffeners =  1 \n"]
    input_file.writelines(stiffening_preamble)
    for i in range(len(stiffeners_ebp)):
        stiffening = "    - Stiffener n° " + str(i) + " Active=1 \n",\
                     "      Orientation = 0 \n",\
                     "      Location    = 100. \n",\
                     "      Gamma       = 25.46 \n",\
                     "      Teta        = 5.487 \n",\
                     "      Delta       = 0.107 \n",\
                     "      Type        =  0 \n",\
                     "      Dimension 1 = 0 \n",\
                     "      Dimension 2 = 0 \n",\
                     "      Dimension 3 = 0 \n",\
                     "      Dimension 4 = 0 \n"]
        input_file.writelines(stiffening)
    stresses = ["#STRESSES \n",\
                "Longitudinal stresses : User's data No \n",\
                 "Analytical Longitudinal stresses \n",\
                  "Imposed values : No \n",\
                   "Longitudinal Stress Top Left                " + str(sigma_a) + " MPa \n",\
                   "Longitudinal Stress Bottom Left             " + str(sigma_b) + " MPa \n",\
                   "Longitudinal Stress Top Right               " + str(sigma_a) + " MPa \n",\
                   "Longitudinal Stress Bottom Right            " + str(sigma_b) + " MPa \n",\
                 "Transverse stresses : User's data No \n",\
                 "Analytical Transverse stresses \n",\
                  "Imposed values : No \n",\
                   "Transverse stress Top                         0.000 MPa \n",\
                   "Transverse stress Bottom                      0.000 MPa \n",\
                   "Patch Load Stress Top                         0.000 MPa \n",\
                   "Patch Load Stress Bottom                      0.000 MPa \n",\
                   "Patch Load Width Top                          0.000 cm \n",\
                   "Patch Load Width Bottom                       0.000 cm \n",\
                   "Local longitudinal stresses under patch load : No \n",\
                   "Local shear stresses under patch load : Yes \n",\
                   "W Top                      -1.000 \n",\
                   "W Bot                      -1.000 \n",\
                   "Shear distribution  1 \n",\
                 "Shear stresses : User's data No \n",\
                 "Analytical Shear stresses \n",\
                  "Imposed values : No \n",\
                   "Shear stress                                 0.000 MPa \n"]
    input_file.writelines(stresses)
    parameters = ["#PARAMETERS \n",\
                   "Complexity : 1 \n",\
                   "Effective width parameter :  10.000"]
    input_file.writelines(parameters)
    input_file.close()

    #run ebplate calculation from your own directory
    os.system(r'"C:\Program Files (x86)\EBPlate\EBPlate.exe" /BATCH C:\Users\Nino\Google Drive\Studium\FS 2021\Bachelorarbeit\BA\ebplate\plate.EBP')

    #get phi_cr from the ebplate.EBR
    result_file = open('ebplate\plate.EBR', 'r')
    results_text = result_file.readlines()
    phi_cr_line = results_text[1]
    phi_cr = float(phi_cr_line[7:])

    return phi_cr
