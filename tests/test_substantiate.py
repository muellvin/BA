import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

from optimizer import substantiate as ss
from classes import proposed_stiffener as ps

proposition = ps.proposed_stiffener(2,1,0, 5*10**6)

ss.find_dimensions_2(proposition)
