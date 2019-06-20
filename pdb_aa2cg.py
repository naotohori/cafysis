#!/usr/bin/env python

from cafysis.file_io.pdb import PdbFile
from cafysis.elements.pdb import Chain, Residue, Atom
from cafysis.elements.coord import Coord

import sys

if len(sys.argv) != 3:
    print('Usage: SCRIPT [input aa PDB] [output cg PDB]')
    sys.exit(2)

ATOMS_P = ('P', 'OP1', 'OP2')

aa = PdbFile(sys.argv[1])
aa.open_to_read()
chains = aa.read_all()

cg_chains = []

res_id = 0
atom_id = 0
for c in chains:
    c_cg = Chain()
    #xyz_O3 = None
    for ir, r in enumerate(c.residues):
        xyz_P = Coord()
        nP = 0
        #if not xyz_O3 is None:
        #    xyz_P += xyz_O3
        #    nP += 1
        #    xyz_O3 = None
        xyz_S = Coord()
        nS = 0 
        xyz_B = Coord()
        nB = 0

        for a in r.atoms:
            name = a.name.strip()
            if name[0] == 'H':
                continue
            #elif name == "O3'":
            #    xyz_O3 = a.xyz
            elif name in ATOMS_P:
                xyz_P += a.xyz
                nP += 1
            elif name.find("'") != -1:
                xyz_S += a.xyz
                nS += 1
            else:
                xyz_B += a.xyz
                nB += 1
            nt = a.res_name.strip()

        res_id += 1
        r_cg = Residue()

        if ir != 0:
            atom_id += 1
            a = Atom()
            a.serial = atom_id
            a.name = ' P  '
            a.res_name = 'R%s ' % nt
            a.chain_id = 'A'
            a.res_seq = res_id
            a.xyz = xyz_P / float(nP)
            r_cg.push_atom(a)

        atom_id += 1
        a = Atom()
        a.serial = atom_id
        a.name = ' S  '
        a.res_name = 'R%s ' % nt
        a.chain_id = 'A'
        a.res_seq = res_id
        a.xyz = xyz_S / float(nS)
        r_cg.push_atom(a)

        atom_id += 1
        a = Atom()
        a.serial = atom_id
        a.name = ' %sb '  %  nt
        a.res_name = 'R%s ' % nt
        a.chain_id = 'A'
        a.res_seq = res_id
        a.xyz = xyz_B / float(nB)
        r_cg.push_atom(a)

        c_cg.push_residue(r_cg)

    cg_chains.append(c_cg)

cg = PdbFile(sys.argv[-1])
cg.open_to_write()
cg.write_all(cg_chains)
cg.close()
