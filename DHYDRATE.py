import numpy as np
from optparse import OptionParser
import os
import sys

parser=OptionParser()
parser.add_option("-f", "--gro", action="store", type='string', dest="InputFile", default='test_SOLV.gro', help="Name of the input gro file.")
parser.add_option("-r", "--ref", action="store", type='string', dest="Reference", default='N31', help="Name of the atom used as a reference.")
parser.add_option("-n", "--totres", action="store", type='string', dest="TotRes", default='768', help="Total number of lipid residues.")
parser.add_option("-o", "--out", action="store", type='string', dest="OutputFile", default='test_SOLV_SFU.gro', help="Name of the output gro file.")
(options, args)= parser.parse_args()
inname_opt=options.InputFile
ref_opt=options.Reference
n_res_opt=int(options.TotRes) #Number of residues that are not SOL
outname_opt=options.OutputFile

def dhydrate(gro_file_func):
    temp_file=open("temp.gro", "a")
    gro_file=np.genfromtxt(gro_file_func, dtype='str', delimiter="\n")
    N_gro=len(gro_file)
    save=0
    Z_box_half=float(gro_file[-1].split()[2])/2.
    Z_up=np.array([])
    Z_down=np.array([])
    for i in range(N_gro-1):
        if "SOL" in gro_file[i]:
            save=i
            break
        if i==0 or i==1:
            temp_file.write(gro_file[i] + "\n")
        else:
            temp_file.write(gro_file[i].rjust(44)+"\n")
            if ref_opt in gro_file[i]:
                Z_val=float(gro_file[i].split()[-1])
                if Z_val>Z_box_half:
                    Z_up=np.append(Z_up, Z_val)
                if Z_val<Z_box_half:
                    Z_down=np.append(Z_down, Z_val)
    lim_up=np.average(Z_up)
    lim_down=np.average(Z_down)
    cont=4
    delta=0
    atom=save-2
    for i in range(save,N_gro-1):
        line_act=gro_file[i].split()
        Z_val = float(line_act[-1])
        if (Z_val > lim_up or Z_val < lim_down) and delta%3==0:
            next_line=gro_file[i+1].split()
            next_line2=gro_file[i+2].split()
            atom+=1
            temp_file.write(str(cont).rjust(5)+"SOL".ljust(5)+"OW".rjust(5)+str(atom%100000).rjust(5)+line_act[-3].rjust(8)+line_act[-2].rjust(8)+line_act[-1].rjust(8)+"\n")
            atom+=1
            temp_file.write(str(cont).rjust(5)+"SOL".ljust(5)+"HW1".rjust(5)+str(atom%100000).rjust(5)+next_line[-3].rjust(8)+next_line[-2].rjust(8)+next_line[-1].rjust(8)+"\n")
            atom+=1
            temp_file.write(str(cont).rjust(5)+"SOL".ljust(5)+"HW2".rjust(5)+str(atom%100000).rjust(5)+next_line2[-3].rjust(8)+next_line2[-2].rjust(8)+next_line2[-1].rjust(8)+"\n")

            cont+=1
        delta+=1
    temp_file.write(gro_file[-1]+"\n")
    temp_file.close()

    temp_file=np.genfromtxt("temp.gro", dtype="str", delimiter="\n")
    N=atom+3
    final_output=open(outname_opt, "a")
    for i in range(N):
        if i==1:
            final_output.write(str(atom)+"\n")
        elif i==N-1:
            final_output.write(temp_file[i].rjust(30))
        else:
            final_output.write(temp_file[i].rjust(44)+"\n")
    final_output.close()
    os.remove("temp.gro")
    print("The system has: "+str(cont-1+n_res_opt/3.)+ " residues")
    print("The system has: "+str(cont-4)+ " water molecules. Change this to the top file")
    print("The system has a lipid:water ratio of: "+str((cont-1)/(n_res_opt/3)))

dhydrate(inname_opt)
