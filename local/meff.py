#!/usr/bin/env python3
import numpy as np
import xml.etree.ElementTree as ET

def get_xml_info(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    # Initialize arrays for storing data
    k_points = []
    eigenvalues = []
    occupations = []
    atomic_structure_tag = root.find(".//atomic_structure")
    
    if atomic_structure_tag is not None:
        alat = atomic_structure_tag.attrib.get('alat')
        alat= float(alat)
    else:
        return None

    for ks_energy in root.findall(".//ks_energies"):
        # Extract k_point
        k_point_tag = ks_energy.find(".//k_point")
        kx, ky, kz = map(float, k_point_tag.text.split())  # Get the k_point values
        
        # Append to k_points
        k_points.append([kx, ky, kz])
        
        # Check if it's the required k_point (0.0, 0.0, 0.0)
        #if [kx, ky, kz] == [0.0, 0.0, 0.0]:
        # Extract eigenvalues and occupations
        eigenval_tag = ks_energy.find(".//eigenvalues")
        occ_tag = ks_energy.find(".//occupations")
        
        if eigenval_tag is not None and occ_tag is not None:
            eigenval_list = list(map(float, eigenval_tag.text.split()))
            occ_list = list(map(float, occ_tag.text.split()))
            
            eigenvalues.append(np.array(eigenval_list))
            occupations.append(np.array(occ_list))
    
    # Convert to numpy arrays for further analysis
    k_points = np.array(k_points)
    eigenvalues = np.array(eigenvalues)
    occupations = np.array(occupations)
    return k_points, eigenvalues*27.211386245981, alat*0.529177210544, occupations

def meff_kpoints_eigenvalues(k_points,eigenvalues,a,index):
    #homo_i=np.sum(occupations[0])
    del_E=(eigenvalues[1,index]-eigenvalues[0,index])
    del_k=np.linalg.norm(k_points[1]-k_points[0])
    e_el=1.602176634*10**-19
    a*=10**-10
    hbar=1.054571817*10**-34
    m_e=9.1093837139*10**-31
    #print(hbar, del_E,e_el,a,del_k)
    meff=(hbar**2/(2*del_E*e_el)) * ((2*np.pi/a)*del_k)**2
    meff/=m_e
    return meff

if __name__=="__main__":
    k_points1,eigenvalues1,a,occupations1=get_xml_info('GaAs/tmp/In0.0Ga1.0As1.0Sb0.0_prim.xml')
    k_points,eigenvalues,a,occupations=get_xml_info('GaAs/meff/In0.0Ga1.0As1.0Sb0.0_prim.xml')
    homo_i=int(int(np.sum(occupations1[0]))-1)
    #print(homo_i)
    #print(k_points.shape,eigenvalues.shape,a,occupations.shape)
    meff_kpoints_eigenvalues(k_points,eigenvalues,a,homo_i+1)
    #print(k_points.shape,eigenvalues.shape,occupations.shape)