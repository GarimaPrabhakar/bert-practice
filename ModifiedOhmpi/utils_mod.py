import numpy as np
import pandas as pd

def scheme_txt2csv(fn):

	with open(fn) as f:
        lines = f.readlines()

    start = lines.index('# a b m n r\n')
    scheme = lines[start:]
    scheme = [a.replace("\t", ",") for a in scheme]

    with open('scheme.csv','w') as result_file:
	    wr = csv.writer(result_file, dialect='excel')
	    wr.writerows(scheme)
