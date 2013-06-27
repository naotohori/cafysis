#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Naoto Hori
'''

from cafysis.elements.coord import Coord
from cafysis.elements.error import Error
from cafysis.elements.pdb import Atom, Chain, Residue

class PdbFile(object) :
    def __init__(self, filename):
        self._filename = filename
        self._status = 'Closed'
        self.flg_HETATM = False
        
    def open_to_read(self):
        if self._status != 'Closed' :
            raise Error('PdbFile', 'open_for_read', 'file is not closed')
        self._file = open(self._filename, 'r')
        
    def open_to_write(self):
        if self._status != 'Closed' :
            raise Error('PdbFile', 'open_for_read', 'file is not closed')
        self._file = open(self._filename, 'w')

    def close(self):
        self._file.close()
        
    def read_all(self):
        chains = []
        c = Chain()
        r = Residue()
        res_seq_pre = -1
        ins_code_pre = -1
        for line in self._file :
            head = line[0:6]
            
            if   head == 'MODEL ' : 
                pass
            
            elif head == 'ATOM  ' or (head == 'HETATM' and self.flg_HETATM):
                a = self._line2atom(line)
                #a.show()
                if a.res_seq != res_seq_pre or a.ins_code != ins_code_pre :
                    if len(r.atoms) != 0 :
                        c.push_residue(r)
                        r = Residue()
                    res_seq_pre = a.res_seq
                    ins_code_pre = a.ins_code
                r.push_atom(a)
                    
            elif (head[:3] == 'TER') or (head[:3] == 'END') or (head[:2] == '>>') :
                if len(r.atoms) != 0:
                    c.push_residue(r)
                    r = Residue()
                if len(c.residues) != 0:
                    chains.append(c)
                    c = Chain()
                
        if len(r.atoms) != 0 :
            c.push_residue(r)
        if len(c.residues) != 0:
            chains.append(c)
        
        return chains
                
    def write_all(self, chains):
        ichain = 0
        for chain in chains :
            ichain += 1
            for i in xrange(chain.num_atom()) :
                line = self._atom2line(chain.get_atom(i))
                self._file.write(line+'\n')
            if ichain < len(chains) :
                self._file.write('TER\n')
                
        self._file.write('END')
        
    def _line2atom(self, line):
        line = line.rstrip()
        if line[0:6] != 'ATOM  ' and line[0:6] != 'HETATM' :
            raise Error('PdbFile', 'decompose_atom', 'line does not begin with "ATOM"')
        
        atom = Atom()
        atom.serial = int(line[6:11])
        atom.name = line[12:16]
        atom.alt_loc = line[16:17]
        atom.res_name = line[17:20]
        atom.chain_id = line[21:22]
        atom.res_seq = int(line[22:26])
        #atom.ins_code = line[26:27]
        atom.ins_code = line[26:30]
        atom.xyz = Coord(float(line[30:38]), float(line[38:46]), float(line[46:54]))
        try :
            atom.occupancy = float(line[54:60])
        except :
            atom.occupancy = 0.0
        try :
            atom.temp_factor = float(line[60:66])
        except :
            atom.temp_factor = 0.0
        atom.element = line[76:78]
        try :
            atom.charge = int(line[78:80])
        except :
            atom.charge = 0
        
        return atom
    
    def _atom2line(self, atom):
        line = ''
        line += 'ATOM  '  # 1-6
        line += '%5i' % (atom.serial,)  # 7-11
        line += ' '  # 12
        line += '%4s' % (atom.name,)    # 13-16
        line += '%1s' % (atom.alt_loc,) # 17
        line += '%3s' % (atom.res_name,) # 18-20
        line += ' '  # 21
        line += '%1s' % (atom.chain_id,)  # 22
        # bugfix 2011/05/05
        #line += '%3i ' % (atom.res_seq,)
        #line += atom.ins_code
        #line += '   '
        line += '%4i' % (atom.res_seq,)
        line += '%4s' % (atom.ins_code,)
        line += '%8.3f' % (atom.xyz.x,)
        line += '%8.3f' % (atom.xyz.y,)
        line += '%8.3f' % (atom.xyz.z,)
        line += '%6.2f' % (atom.occupancy,)
        line += '%6.2f' % (atom.temp_factor,)
        line += ' ' * 10
        line += atom.element
        line += '%2i' % (atom.charge,)
        
        return line
            
