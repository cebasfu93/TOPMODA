import numpy as np
from optparse import OptionParser
import os
import sys

parser=OptionParser()
parser.add_option("-f", "--gro", action="store", type='string', dest="InputFile", default='test_SOLV.gro', help="Name of the input gro file.")
parser.add_option("-R", "--radius", action="store", type='float', dest="Radius", default='1.25', help="Radius in nm of the sphere to exclude water from.")
parser.add_option("-n", "--nres", action="store", type='int', dest="N_Res", default='0', help="Number of non-PW residues.")
parser.add_option("-r", "--ref", action="store", type='string', dest="Reference", default='Pt', help="Name of the atom used as a reference.")
parser.add_option("-o", "--out", action="store", type='string', dest="OutputFile", default='test_HYDRA.gro', help="Name of the output gro file.")
(options, args)= parser.parse_args()
inname_opt=options.InputFile
rad_opt = options.Radius
N_res_opt = options.N_Res
ref_opt=options.Reference
outname_opt=options.OutputFile

def dhydrate_CG():
    temp_file = open("temp.gro", "w")
    gro_file = np.genfromtxt(inname_opt, dtype='str', delimiter="\n")
    N_gro = len(gro_file)
    save = 0
    x_ref = []
    for i in range(N_gro):
        if "PW" in gro_file[i]:
            save = i
            break
        if i==0 or i==1:
            temp_file.write(gro_file[i]+"\n")
        else:
            temp_file.write(gro_file[i].rjust(44)+"\n")
            if ref_opt in gro_file[i]:
                x_ref.append(gro_file[i].split()[-3:])

    x_ref = np.array(x_ref, dtype='float')
    x_center = np.average(x_ref, axis=0)

    delta = 0
    atom = save-2
    cont = N_res_opt + 1
    for i in range(save, N_gro-1):
        line_act = gro_file[i].split()
        rad = np.linalg.norm(np.array(line_act[-3:], dtype='float')-x_center)
        if rad > rad_opt and delta%3 == 0:
            next_line = gro_file[i+1].split()
            next_line2 = gro_file[i+2].split()
            #cont=1 ########################################
            atom+=1
            temp_file.write(str(cont).rjust(5) + "PW".ljust(5) + "W".rjust(5) + str(atom%100000).rjust(5) + line_act[-3].rjust(8)+line_act[-2].rjust(8)+line_act[-1].rjust(8)+"\n")
            atom+=1
            temp_file.write(str(cont).rjust(5) + "PW".ljust(5) + "WP".rjust(5) + str(atom%100000).rjust(5) + next_line[-3].rjust(8)+next_line[-2].rjust(8)+next_line[-1].rjust(8)+"\n")
            atom+=1
            temp_file.write(str(cont).rjust(5) + "PW".ljust(5) + "WM".rjust(5) + str(atom%100000).rjust(5) + next_line2[-3].rjust(8)+next_line2[-2].rjust(8)+next_line2[-1].rjust(8)+"\n")

            cont+=1
        delta += 1
    temp_file.write(gro_file[-1]+"\n")
    temp_file.close()

    temp_file=np.genfromtxt("temp.gro", dtype="str", delimiter="\n")
    N=atom+3
    final_output=open(outname_opt, "w")
    for i in range(N):
        if i==1:
            final_output.write(str(atom)+"\n")
        elif i==N-1:
            final_output.write(temp_file[i].rjust(30))
        else:
            final_output.write(temp_file[i].rjust(44)+"\n")
    final_output.close()
    os.remove("temp.gro")


dhydrate_CG()
