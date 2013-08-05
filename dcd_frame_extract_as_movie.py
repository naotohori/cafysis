#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011/03/17 (dcd_frame_extract.py)
Added stride mode on 2011/07/29 (dcd_frame_extract.py)
Modified from dcd_frame_extract.py on 2011/12/20
@author: Naoto Hori
'''

import sys
from cafysis.file_io.dcd import DcdFile
from cafysis.file_io.pdb import PdbFile

if (not len(sys.argv) in (6, 7)):
    print 'Usage: % SCRIPT [input DCD] [beginning (0)] [end] [reference PDB] [output movie]'
    print '       % SCRIPT [input DCD] [beginning (0)] [end] [stride] [reference PDB] [output movie]'
    sys.exit(2)

frame_begin = int(sys.argv[2])
if frame_begin < 0:
    print 'Error: beginning frame should not less than 0'
    sys.exit(2)
frame_end = int(sys.argv[3])
if (len(sys.argv) == 6) :
    frame_stride = 1
else:
    frame_stride = int(sys.argv[4])
    if frame_stride <= 0:
        print 'The frame stride is invalid'
        sys.exit(2)
        
frame_num = frame_end - frame_begin + 1
if frame_num < 1 :
    print 'The number of frames is invalid.'
    sys.exit(2)


# Read the reference PDB
pdb = PdbFile(sys.argv[-2])
pdb.open_to_read()
chains = pdb.read_all()
pdb.close()

# Output PDB
pdb = PdbFile(sys.argv[-1])
pdb.open_to_write()


# Open DCD and read the header
dcd_filename = sys.argv[1]
dcd = DcdFile(dcd_filename)
dcd.open_to_read()
dcd.read_header()

def error_no_data() :
    print 'The number of frames is invalid.'
    print 'Header information:'
    dcd.show_header()
    sys.exit(2)

# skip
dcd.skip(frame_begin - 1)
i_org = frame_begin

# read and write
icount = -1
for i in xrange(frame_num) :
    if not dcd.has_more_data() :
        error_no_data()
        
    icount += 1
    if icount % frame_stride == 0 :
        icount = 0
    else :
        dcd.skip(1)
        i_org += 1
        continue
    
    struct = dcd.read_onestep()
    iatom = 0
    for c in chains:
        for r in c.residues:
            for a in r.atoms:
                a.xyz.put_as_list(struct[iatom])
                iatom += 1
    pdb.modelID = i
    pdb.set_remark('ORIGINAL_FILE %s' % (dcd_filename,))
    pdb.set_remark('ORIGINAL_FRAME %i' % (i_org,))
    pdb.write_all(chains)
    i_org += 1

dcd.close()
pdb.close()
