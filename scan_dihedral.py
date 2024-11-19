from openbabel import pybel

A, B, C, D = 40, 39, 34, 35
# Load molecule using Pybel
mol = next(pybel.readfile("pdb", "3.pdb"))
atom1, atom2, atom3, atom4 = mol.atoms[A - 1], mol.atoms[B - 1], mol.atoms[C - 1], mol.atoms[D - 1]

# Calculate the initial dihedral angle between these four atoms
dihedral_angle = mol.OBMol.GetTorsion(atom1.OBAtom, atom2.OBAtom, atom3.OBAtom, atom4.OBAtom)
print(f"The initial dihedral angle is {dihedral_angle:.2f} degrees.")

# Create a single Notepad text file to store all entries
notepad_filename = "terachem_input_all.txt"
with open(notepad_filename, 'w') as notepad_file:
    # Rotate dihedral angle and create corresponding .xyz and .ts files
    for target_angle in range(-140, 51, 10):
        mol.OBMol.SetTorsion(atom1.idx, atom2.idx, atom3.idx, atom4.idx, target_angle)
        dihedral_angle = mol.OBMol.GetTorsion(atom1.OBAtom, atom2.OBAtom, atom3.OBAtom, atom4.OBAtom)
        
        # Save modified structure as .xyz file
        xyz_filename = f"modified_dihedral_{dihedral_angle:.1f}.xyz"
        mol.write("xyz", xyz_filename)
        
        # Create corresponding .ts file with specified content
        ts_filename = f"modified_dihedral_{dihedral_angle:.1f}.ts"
        ts_content = f"""basis    def2-SVP
coordinates    {xyz_filename}
charge          0
spinmult      1
method          wb97xd3
dispersion d3
rc_w 0.06620546488120216
pcm cosmo
epsilon 2.38
pcm_scale 1
maxit 500
solvent_radius 3.48
run energy
end
"""
        # Write .ts file
        with open(ts_filename, 'w') as ts_file:
            ts_file.write(ts_content)

        # Write the line to the Notepad file
        notepad_file.write(f"terachem /scr/user/woon/3_5_7/{ts_filename}\n")

        print(f"Generated {xyz_filename} and {ts_filename} for target angle {target_angle} degrees.")

print(f"All terachem commands have been written to {notepad_filename}.")
