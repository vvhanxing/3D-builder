import re
import os

from collections import OrderedDict



ATOM_type_list =[

    (0.1,"H"),
    (0.2,"C"),
    (0.3,"N"),
    (0.4,"O"),
    (0.5,"F"),
    (0.6,"P"),
    (0.7,"S"),
    (0.8,"Cl"),
    (0.9,"Br"),
    (1.0,"I"),
    (1.1,"Other")]

colors_list=['ghostwhite',
            'grey',
            'blue',
            'red',
            'cyan',
            'darkorange',
            'yellow',
            'lime',
            'darkred',
            'purple',
            'black'
                     ]
ATOMdecode = OrderedDict(ATOM_type_list)

def getLineElement(file_name):     #找到文件每行元素输出为二维列表

    mode=file_name[-3:]

    with open(file_name,"r") as txt:
        
        pattern = re.compile(r'\S+')
        
        lines_info_list=[]
        
        for line in txt.readlines():

            lines_info_list.append ( pattern.findall(line))
    
    return lines_info_list ,mode







def get_mol_info(file_name):     #将输入的二维文本列表转化为原子类型，原子坐标，键连关系

    
    Lines,mode = getLineElement(file_name)
    
    if mode == "sdf" or mode == "mol":
        atom_info = []
        atom_bond = []
        for cont, line in enumerate( Lines):
            #print(cont,line)
        
            if len(line)==16:
            
                atom_info .append(line)
            if len(line)==7:
                        
                atom_bond .append(line[:2])
            bond_line_str=""
            if len(line)==6:
                #print(line)
                if len(line[0])==4:           
                    bond_line_str="  "+line[0]
                    #print(bond_line_str[:3],"-----", bond_line_str[3:])
                    atom_bond .append( [   bond_line_str[:3], bond_line_str[3:]   ])
                if len(line[0])==5:           
                    bond_line_str=" "+line[0]
                    #print(bond_line_str[:3],"-----", bond_line_str[3:])
                    atom_bond .append( [   bond_line_str[:3], bond_line_str[3:]   ])
                if len(line[0])==6:           
                    bond_line_str=""+line[0]
                    #print(bond_line_str[:3],"-----", bond_line_str[3:])
                    atom_bond .append( [   bond_line_str[:3], bond_line_str[3:]   ])
                    
        #atom_type = {}
        atom_type= OrderedDict([])





        
        for count,i in enumerate (atom_info):      
        


            for ATOM_type in  ATOM_type_list:
                if   ATOM_type[1] == i[3]:
                    atom_type[str(count+1)] = (ATOM_type[1],ATOM_type[0])
                if i[3] not in list(zip(*ATOM_type_list))[1]:
                    print(i[3])
                    atom_type[str(count+1)] = ("Other",1.1)
                    

  
            
        atom_pos = []
        for i in atom_info:
            atom_pos.append(  (float(i[0]),float(i[1]),float(i[2]))   )

        atom_bond_=[]

        for i in range(1,len(atom_pos)+1):
            for j in atom_bond:

                if str(i) in j:
                    b = sorted([int (x) for x in  j])
                    b_= [str(x) for x in  b]
                    atom_bond_.append(b_)
    
        atom_bond__=[]
        for i in atom_bond_:
            if i not in atom_bond__:
                #i.insert(0,str(count+1))
                atom_bond__.append(i)
                #print(count)
        def take_band_pos_first(elem):
            return int(elem[0])
        atom_bond__ .sort(key=take_band_pos_first)
    
        atom_bond___=[]
        for count,i in enumerate(atom_bond__):
            i.insert(0,str(count+1))
            i.insert(3,str(1))
            atom_bond___.append(i)

        return atom_type , atom_pos, atom_bond___ 


    if mode ==  "ol2":
        atom_num_mark = 0
        atom_pos_mark_start = 0
        atom_pos_mark_end = 0
        atom_bond_mark_start = 0
        atom_bond_mark_end = 0
    
        for cont, line in enumerate( Lines):
            #print(cont,line)
        
            if "@<TRIPOS>MOLECULE" in str(line):
            
                atom_num_mark = cont+2
                #print(atom_num_mark)
            if "@<TRIPOS>ATOM" in str(line):
            
                atom_pos_mark_start = cont + 1
                atom_pos_mark_end = cont + 1 + int(Lines[atom_num_mark][0])
            
                #print(atom_pos_mark_start,atom_pos_mark_end)
        
            if "@<TRIPOS>BOND" in str(line):
            
                atom_bond_mark_start = cont + 1
                atom_bond_mark_end = cont + 1 + int(Lines[atom_num_mark][1])
                #print(atom_bond_mark_start,atom_bond_mark_end)

        atom_info = Lines[atom_pos_mark_start:atom_pos_mark_end]

        atom_bond = Lines[atom_bond_mark_start:atom_bond_mark_end]
    
        #atom_type = {}
        atom_type= OrderedDict([])


        #print(atom_info )
        for i in atom_info:      #尽管C 与 Cl 都含有C，但键只能对应一个值，所以会在后面的判断中改正

            
        




            for ATOM_type in  ATOM_type_list:
                
                if   ATOM_type[1] in i[1]:
                    atom_type[i[0]] = (ATOM_type[1],ATOM_type[0])
                    



            if "H" not in i[1] and "C" not in i[1]and "N" not in i[1]and"O"not in i[1]and "F"not in i[1]and"P"not in i[1]and"S"not in i[1]and"Cl"not in i[1]and"Br"not in i[1]and"I" not in i[1]:
                print(i[1])
                atom_type[i[0]] = ("Other",1.1 )
            
        atom_pos = []
        for i in atom_info:
            atom_pos.append(  (float(i[2]),float(i[3]),float(i[4]))   )

        return atom_type ,atom_pos,atom_bond 


if __name__=="__main__":
    file_name = "new1.mol2"
    print(get_mol_info(file_name)[0])
    print(get_mol_info(file_name)[1])
    print(get_mol_info(file_name)[2])


