import math

#machine settings
filament_d=1.75 #filament diameter, mm, always more than 0
nozzle_d=0.4 #nozzle diameter, mm, always more than 0
filament_flow=1 #flow, always more than 0

#filament settings
retract_fr=30 #retract speed, mm/sec, always more than 0
retract=2 #retract amount, mm, always 0 or more
linear_adv=-1 #linear advance value, negative to disable
nozzle_temp=215 #nozzle temp, C, as reccommended by filament
bed_temp=60 #bed temp, C, what works best for filament, 0 to disable

#cali settings
layer_h=0.2 #default layer height, mm, always more than 0, half nozzle_d rounded down to nearest step for best results
z_diff=0.1 #max extra Z to test, mm, always more than 0, 50 to 75% of layer_h idealy

#bed center position (mm)
cent_x=150
cent_y=150

#template params
temp_noz_d=0.4
temp_w=97.636

def calc_e(l,lh,ew,flow,fil_d):
    return (lh*flow*ew*l)/(math.pi/4*(fil_d**2))

def scale_translate_gcode(gcode,scale,x,y,x1,y1):
    if gcode.startswith("G1") and "X" in gcode:
        x2=float(gcode[gcode.index("X")+1:gcode.index(" ",gcode.index("X"))].replace("-.","-0."))*scale+x
        y2=float(gcode[gcode.index("Y")+1:gcode.index(" ",gcode.index("Y"))].replace("-.","-0."))*scale+y
        dist=math.sqrt(((x1-x2)**2)+((y1-y2)**2))
        return [gcode[:gcode.index("X")+1]+str(round(x2,5))+" Y"+str(round(y2,5))+gcode[gcode.index(" ",gcode.index("Y")):],x2,y2,dist]
    return [line,x1,y1,-1]

if __name__=="__main__":
    with open("template.txt") as fr:
        fw=open("z cali.gcode","w+",newline="\n")
        lines=fr.readlines()
        scale=nozzle_d/temp_noz_d
        cur_x=0
        cur_y=0
        cur_e=0
        temp=""
        for line in lines:
            if line.startswith("G1"):
                move=scale_translate_gcode(line,scale,cent_x,cent_y,cur_x,cur_y)
                temp_e=0
                if move[3]>0:
                    temp_e=calc_e(move[3],layer_h,nozzle_d,filament_flow,filament_d)
                cur_x=move[1]
                cur_y=move[2]
                cur_e+=temp_e
                temp=move[0]
                if "[z_cali]" in temp:
                    temp=temp.replace("[z_cali]",str(round(layer_h+((cur_x-cent_x+temp_w*scale/2)/scale/temp_w*z_diff),5)))
                if "[z_init]" in temp:
                    temp=temp.replace("[z_init]",str(round(layer_h,5)))
                if "[extrude]" in temp:
                    temp=temp.replace("[extrude]",str(round(cur_e,5)))
                if "[ret]" in temp:
                    temp=temp.replace("[ret]",str(round(retract,5)))
                if "[ret_fr]" in temp:
                    temp=temp.replace("[ret_fr]",str(round(retract_fr*60,5)))
            elif line.startswith("G92 E0"):
                cur_e=0
                temp=line
            elif "[lin_adv]" in line:
                if linear_adv>=0:
                    temp=line.replace("[lin_adv]",str(round(linear_adv,5)))
                else:
                    continue
            elif "[bed_temp]" in line:
                temp=line.replace("[bed_temp]",str(round(bed_temp,5)))
            elif "[noz_temp]" in line:
                temp=line.replace("[noz_temp]",str(round(nozzle_temp,5)))
            elif ";keep" in line:
                temp=line
            else:
                continue
            fw.write(temp)        
        fw.close()
