#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import numpy as np

def read_qe_xml(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Initialize arrays for storing data
    k_points = []
    eigenvalues = []
    occupations = []
    
    # Navigate to the ks_energies sections
    for ks_energy in root.findall(".//ks_energies"):
        # Extract k_point
        k_point_tag = ks_energy.find(".//k_point")
        kx, ky, kz = map(float, k_point_tag.text.split())  # Get the k_point values
        
        # Append to k_points
        k_points.append([kx, ky, kz])
        
        # Check if it's the required k_point (0.0, 0.0, 0.0)
        if [kx, ky, kz] == [0.0, 0.0, 0.0]:
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
    return k_points, eigenvalues, occupations

# Example usage
def get_Eg_xml(xml_file):
    #xml_file = 'In3Ga1Sb/tmp/In0.75Ga0.25As0.0Sb1.0_square_rep_20.xml'  # Replace with the path to your XML file
    k_points, eigenvalues, occupations = read_qe_xml(xml_file)
    homo_ind=np.sum(occupations[0])-1
    homo_ind=int(homo_ind)
    #print(eigenvalues.shape)
    #homo_eigs=eigenvalues[occupations>0.5]
    #lomo_eigs=eigenvalues[occupations<0.5]
    Eg=eigenvalues[0,homo_ind+1]-eigenvalues[0,homo_ind]
    Eg_eV=Eg*27.2114
    return Eg_eV

