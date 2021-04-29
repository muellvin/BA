import sys
sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')
from classes import crosssection
import cs_collector


cs1 = crosssection.crosssection(0,0,0)
cs1.cost = 4
cs_collector.into_collector(cs1)

cs2 = crosssection.crosssection(0,0,0)
cs2.cost = 2
cs_collector.into_collector(cs2)

cs3 = crosssection.crosssection(0,0,0)
cs3.cost = 2
cs_collector.into_collector(cs3)

cs4 = crosssection.crosssection(0,0,0)
cs4.cost = 2
cs_collector.into_collector(cs4)



best = cs_collector.get_best()
for i in best:
    print(i.cost)
