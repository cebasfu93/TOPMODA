import numpy as np
from optparse import OptionParser
import os
import sys

parser=OptionParser()
parser.add_option("-f", "--gro", action="store", type='string', dest="InputFile", default='test_SOLV.gro', help="Name of the input gro file.")
parser.add_option("-o", "--out", action="store", type='string', dest="OutputFile", default='test_SOLV_RENUM.gro', help="Name of the re-enumerated output gro file.")
(options, args)= parser.parse_args()
inname_opt=options.InputFile
outname_opt=options.OutputFile
last_char=-34
def renum(gro_file_func):
    gro_file=np.genfromtxt(gro_file_func, delimiter="\n", dtype="str")
    out_file=open(outname_opt, "a")

    N_gro=len(gro_file)
    N_one=int(gro_file[1])+3

    for i in range(N_gro):
        if i%N_one==0 or i%N_one ==1 or i%N_one==(N_one-1):
            out_file.write(gro_file[i]+"\n")
            res_act="PA"
            atom=1
            residue=1
        else:
            line_act=gro_file[i]
            res_prev=res_act
            if "PA" in line_act:
                res_act="PA"
                if res_act!=res_prev:
                    residue+=1
                out_file.write(str(residue).rjust(5)+"PA".ljust(5)+line_act[last_char:]+"\n")
            elif "PC" in line_act:
                res_act="PC"
                if res_act!=res_prev:
                    residue+=1
                out_file.write(str(residue).rjust(5)+"PC".ljust(5)+line_act[last_char:]+"\n")
            elif "OL" in line_act:
                res_act="OL"
                if res_act!=res_prev:
                    residue+=1
                out_file.write(str(residue).rjust(5)+"OL".ljust(5)+line_act[last_char:]+"\n")
    out_file.close()

renum(inname_opt)
