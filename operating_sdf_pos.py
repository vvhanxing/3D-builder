from rdkit import Chem

from rdkit.Chem import AllChem

import numpy as np

def opt_mol_from_smi(smi,save_name):
    """
    opt mol from smiles
    """
    mol = Chem.MolFromSmiles(smi)
 
    
    mol = Chem.AddHs(mol)
    
    AllChem.EmbedMolecule( mol,randomSeed=3 )

    AllChem.MMFFOptimizeMolecule(mol)
    mol = Chem.rdmolops.RemoveHs(mol)

        

    writer = Chem.SDWriter(save_name)
    mol.SetProp('_Name', 'Chemistry '+save_name)
    mol.SetProp('STEREOCHEM', str(1.00))
    mol.SetProp('EF', str(1.00))
    mol.SetProp('MOL_WEIGHT',str(1.00))
    mol.SetProp('COMPOUND_ID',str(1.00))
    mol.SetProp('SUPPLIER',str(1.00))
    mol.SetProp('COMMEN',str(1.00))
    writer.write(mol)
    return save_name+".mol"


        
def operating_sdf_pos(file_name,m,save_file_name):
    """

    """
    with open(file_name,"r") as txt:
        lines = txt.readlines()
        start = 0
        end = 0
        for index, line in enumerate(lines):
            #print(line)
            if "V2000" in line and index+1:
                start = index+1
                end = index+int(line.split()[0])+1
                #print("-----------------------------------",start,end)
        pos = lines[start:end]
        
        pos = [ np.array([float(j) for k, j in  enumerate(i.split()) if k<3 ]) for i in pos ]



    lines_a = lines[:start]
    lines_b = []

    for index ,p in enumerate(pos):

        #print(p)
        p =  p.dot(m)
        p_x  = p[0]
        p_y  = p[1]
        p_z  = p[2]
        #print(str(round(p_z,4)))
        #print( lines[index])
        space_x = " "
        if p_x< 0:
            space_x = ""
        str_x = space_x + str(round(p_x,4))+"0"*(4-len( str(round(p_x,4)).split(".")[1] ))

        space_y = " "
        if p_y< 0:
            space_y = ""
        str_y = space_y + str(round(p_y,4))+"0"*(4-len( str(round(p_y,4)).split(".")[1] ))

        space_z = " "
        if p_z< 0:
            space_z = ""
        str_z = space_z + str(round(p_z,4))+"0"*(4-len( str(round(p_z,4)).split(".")[1] ))


        lines_b.append("   "+str_x+"   "+str_y+"   "+str_z + lines[start+index][30:])  

    #input("")
    lines_c = lines[end:]
    lines = []
    lines.extend(lines_a)    
    lines.extend(lines_b)
    lines.extend(lines_c)

    
    

    with open(save_file_name,"w") as txt:
        txt.writelines(lines )


    return pos


def get_sdf_chiral_center(file_name):
    mols_suppl = Chem.SDMolSupplier(file_name)

    for mol in mols_suppl: 
         # mol3的类型=<class 'rdkit.Chem.rdchem.Mol'>
         #print('类型=',type(mol))  

         Chem.AssignAtomChiralTagsFromStructure(mol)
         # 找到分子的手性中心
         chiral_center = Chem.FindMolChiralCenters(mol) 
         return chiral_center   


def Rotation( theta,aix):
    R = np.ones([3,3])



    if aix == "x":
        R = np.array([[   1, 0,             0            ],
                        [ 0, np.cos(theta),-np.sin(theta)],
                        [ 0, np.sin(theta), np.cos(theta)]])



    if aix == "y":
        R = np.array([[   np.cos(theta), 0, np.sin(theta)],
                        [ 0,             1,            0],       
                        [-np.sin(theta), 0, np.cos(theta)]])
                        


    if aix == "z":
        R = np.array([[  np.cos(theta),-np.sin(theta),0],
                        [np.sin(theta), np.cos(theta),0],
                        [0,             0,            1]])                        
    return R
    
if __name__ == "__main__":




    print("---------------------")
    from math import pi




    with open("smi.txt","r") as TXT:
        lines =  TXT.readlines()
        for index, line in enumerate(lines):

            smi = line[:-1]


            print(index,"--------------------------------------------------")
            save_name = str(index)+".sdf"
            opt_mol_from_smi(smi,save_name)
            s = get_sdf_chiral_center(save_name)
            print("1",s)



            save_mirr_name = save_name+"mirror.sdf"

            m = np.array([[1,0,0],
                          [0,1,0],
                          [0,0,-1]])
            operating_sdf_pos(save_name,m,save_mirr_name)
            s = get_sdf_chiral_center(save_mirr_name) 
            print("2",s)


            
            for i,theta in enumerate( [pi/3,2*pi/3,pi,4*pi/3,5*pi/3,2*pi] ):
            
                save_mirr_rotate_name = save_name+"mirror_rotate"+str(i)+".sdf"

                m = Rotation(theta,"x")
                operating_sdf_pos(save_mirr_name,m,save_mirr_rotate_name)
                s = get_sdf_chiral_center(save_mirr_rotate_name) 
                print(i,s)

            print("--------------------------------------------------")





