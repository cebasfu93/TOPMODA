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

def renum(gro_file_func):
    gro_file=np.genfromtxt(gro_file_func, delimiter="\n", dtype="str")
    temp_file=open("temp.gro", "a")

    N_gro=len(gro_file)
    atom=1
    residue=1
    res_act="PA"
    for i in range(N_gro):
        if i==0 or i ==1 or i==(N_gro-1):
            temp_file.write(gro_file[i]+"\n")
        else:
            line_act=gro_file[i]
            res_prev=res_act
            if "PA" in line_act:
                res_act="PA"
                if res_act!=res_prev:
                    residue+=1
                temp_file.write(str(residue).rjust(5)+"PA".ljust(5)+line_act[-58:]+"\n")
            elif "PC" in line_act:
                res_act="PC"
                if res_act!=res_prev:
                    residue+=1
                temp_file.write(str(residue).rjust(5)+"PC".ljust(5)+line_act[-58:]+"\n")
            elif "SOL" in line_act:
                break
            elif "OL" in line_act:
                res_act="OL"
                if res_act!=res_prev:
                    residue+=1
                temp_file.write(str(residue).rjust(5)+"OL".ljust(5)+line_act[-58:]+"\n")
    temp_file.write(gro_file[-1])
    temp_file.close()

    out_file=open(outname_opt, "a")
    temp_gro=np.genfromtxt("temp.gro", delimiter="\n", dtype="str")
    N_out=len(temp_gro)
    for i in range(N_out):
        if i==1:
            out_file.write(str(N_out-3)+"\n")
        elif i==0 or i==N_out-1:
            out_file.write(temp_gro[i]+"\n")
        else:
            out_file.write(temp_gro[i].rjust(68)+"\n")
    out_file.close()
renum(inname_opt)
