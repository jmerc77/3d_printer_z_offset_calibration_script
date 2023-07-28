import math
# z_cali, z_init, lin_adv, bed_temp, noz_temp, ret_fr, ret, extrude
if __name__=="__main__":
    with open("Z offset box.gcode") as fr:
        fw=open("template.txt","w+",newline="\n")
        lines=fr.readlines()
        cali_moves=False
        temp=""
        min_x=0
        max_x=0
        for line in lines:
            if line.startswith(";TYPE:Solid infill"):
                cali_moves=True
                continue
            elif line[0]==";":
                continue
            if line.startswith("G1"):
                if cali_moves:
                    if "Z" in line:
                        temp=line.replace("Z.2","Z[z_cali]")
                    elif "E" in line and "X" in line:
                        temp=line.replace("E","Z[z_cali] E")
                    else:
                        temp=line
                        if temp.startswith("G10"):
                            temp="G92 E0 ;keep\nG1 E-[ret] F[ret_fr] ;\n"
                        if temp.startswith("G11"):
                            temp="G1 E[ret] F[ret_fr] ;\n"
                        if "X" in temp:
                            temp=temp[:-1]+" ;\n"
                    if "z_cali" in temp and "X" in temp:
                        if "E" in temp:
                            temp=temp[:-len(temp)+temp.index("E")]+"E[extrude] ;move\n"
                        else:
                            temp=temp[:-1]+" ;move\n"
                    if "X" in temp:
                        x=float(temp[temp.index("X")+1:temp.index(" ",temp.index("X"))].replace("-.","-0."))
                        if x<min_x:
                            min_x=x
                        if x>max_x:
                            max_x=x
                else:
                    if "Z" in line:
                        temp=line.replace("Z.2","Z[z_init]")
                    elif "E" in line and "X" in line:
                        temp=line.replace("E","Z[z_init] E")
                    else:
                        temp=line
                        if temp.startswith("G10"):
                            temp="G92 E0 ;keep\nG1 E-[ret] F[ret_fr]\n"
                        if temp.startswith("G11"):
                            temp="G1 E[ret] F[ret_fr]\n"
                        if "X" in temp:
                            temp=temp[:-1]+" ;\n"
                    if "z_init" in temp and "X" in temp:
                        if "E" in temp:
                            temp=temp[:-len(temp)+temp.index("E")]+"E[extrude] ;move\n"
                        else:
                            temp=temp[:-1]+" ;move\n"
            elif line.startswith("M900"):
                temp="M900 K[lin_adv]\n"
            elif line.startswith("M190"):
                temp="M190 S[bed_temp]\n"
            elif line.startswith("M109"):
                temp="M109 S[noz_temp]\n"
            elif line.startswith("G28") or line.startswith("G29") or line.startswith("G92") or line.startswith("M107") or line.startswith("M82") or line.startswith("G21") or line.startswith("M106") or line.startswith("M140") or line.startswith("M104") or line.startswith("M84") or line.startswith("G29") or line.startswith("G90"):
                temp=line[:-1]+" ;keep\n"
            else:
                continue
            fw.write(temp)
        print("temp_w="+str(max_x-min_x))
    fw.close()
