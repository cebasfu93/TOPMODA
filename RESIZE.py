import numpy as np
from optparse import OptionParser
import os
import sys

parser=OptionParser()
parser.add_option("-f", "--gro", action="store", type='string', dest="InputFile", default='test_SOLV.gro', help="Name of the input gro file.")
parser.add_option("-z", "--distz", action="store", type="string", dest="Height", default="3.0", help="High to increase the solvent box.")
parser.add_option("-y", "--disty", action="store", type="string", dest="Width", default="1.0", help="Width (in Y) to decrease the box")
parser.add_option("-x", "--distx", action="store", type="string", dest="Length", default="1.0", help="Length (in X) to decrease the box")
(options, args)= parser.parse_args()
inname_opt=options.InputFile
height_opt=float(options.Height)
width_opt=float(options.Width)
length_opt=float(options.Length)

def resize(gro_file_func):
    gro_file=np.genfromtxt(gro_file_func, dtype='str', delimiter="\n")
    N_gro=len(gro_file)
    for i in range(N_gro):
        if i==N_gro-1:
            box=gro_file[i].split()
            equis="{:.5f}".format(float(box[0])-length_opt)
            ye="{:.5f}".format(float(box[0])-width_opt)
            zeta="{:.5f}".format(float(box[2])+height_opt)
            message=equis.rjust(10)+ye.rjust(10)+zeta.rjust(10)
            print(message)
resize(inname_opt)
