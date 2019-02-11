"""
File input/output functions for molecular geometry files.

Can support XYZ, COLUMBUS and Z-matrix formats. Input and output both
require an open file to support multiple geometries. Only 3D geometries
are currently supported.
TODO: Add custom formats.
"""
import numpy as np
import gimbal.constants as con
import gimbal.displace as displace
import gimbal.measure as measure


def read_xyz(infile, units='ang', hasvec=False, hascom=False):
    """Reads input file in XYZ format.

    XYZ files are in the format:
    natm
    comment
    A X1 Y1 Z1 [Vx1 Vy1 Vz1]
    B X2 Y2 Z2 [Vx2 Vy2 Vz2]
    ...
    where natm is the number of atoms, comment is a comment line, A and B
    are atomic labels and X, Y and Z are cartesian coordinates (in
    Angstroms). The vectors Vx, Vy and Vz are optional and will only be
    read if hasvec = True.

    Due to the preceding number of atoms, multiple XYZ format geometries
    can easily be read from a single file.
    """
    try:
        natm = int(infile.readline())
    except ValueError:
        raise ValueError('Geometry not in XYZ format.')
    if hascom:
        comment = infile.readline().strip()
    else:
        infile.readline()
        comment = ''
    data = np.array([infile.readline().split() for i in range(natm)])
    elem = data[:, 0]
    xyz = data[:, 1:4].astype(float) * con.conv(units, 'ang')
    if hasvec:
        vec = data[:, 4:7].astype(float)
    else:
        vec = None
    return elem, xyz, vec, comment


def read_col(infile, units='bohr', hasvec=False, hascom=False):
    """Reads input file in COLUMBUS format.

    COLUMBUS geometry files are in the format:
    A nA X1 Y1 Z1 mA
    B nB X2 Y2 Z2 mB
    ...
    where A and B are atomic labels, nA and nB are corresponding atomic
    numbers, mA and mB are corresponding atomic masses and X, Y and Z
    are cartesian coordinates (in Bohrs).

    COLUMBUS geometry files do not provide the number of atoms in each
    geometry. A comment line (or blank line) must be used to separate
    molecules.

    For the time being, vector input is not supported for the
    COLUMBUS file format.
    """
    if hascom:
        comment = infile.readline().strip()
    else:
        comment = ''
    data = np.empty((0, 6), dtype=str)
    while True:
        pos = infile.tell()
        line = np.array(infile.readline().split())
        try:
            # catch comment line or end-of-file
            line[1:].astype(float)
            data = np.vstack((data, line))
        except (ValueError, IndexError):
            if len(data) < 1:
                raise ValueError('Geometry not in COLUMBUS format.')
            else:
                # roll back one line before break
                infile.seek(pos)
                break
    elem = data[:, 0]
    xyz = data[:, 2:5].astype(float) * con.conv(units, 'ang')
    if hasvec:
        vec = np.zeros_like(xyz)
    else:
        vec = None
    return elem, xyz, vec, comment


def read_gdat(infile, units='bohr', hasvec=False, hascom=False):
    """Reads input file in FMS90 Geometry.dat format.

    Geometry.dat files are in the format:
    comment
    natm
    A X1 Y1 Z1
    B X2 Y2 Z2
    ...
    Vx1 Vy1 Vz1
    Vx2 Vy2 Vz2
    ...
    where comment is a comment line, natm is the number of atoms, A and B
    are atomic labels, X, Y and Z are cartesian coordinates and Vq are
    vectors for cartesian coordinates q. The vectors are only read if
    hasvec = True.
    """
    if hascom:
        comment = infile.readline().strip()
    else:
        infile.readline()
        comment = ''
    try:
        natm = int(infile.readline())
    except ValueError:
        raise ValueError('geometry not in Geometry.dat format')
    data = np.array([infile.readline().split() for i in range(natm)])
    elem = data[:, 0]
    xyz = data[:, 1:].astype(float) * con.conv(units, 'ang')
    if hasvec:
        vec = np.array([infile.readline().split() for i in range(natm)],
                       dtype=float)
    else:
        vec = None
    return elem, xyz, vec, comment


def read_zmt(infile, units='ang', hasvec=False, hascom=False):
    """Reads input file in Z-matrix format.

    Z-matrix files are in the format:
    A
    B 1 R1
    C indR2 R2 indA2 A2
    D indR3 R3 indA3 A3 indT3 T3
    E indR4 R4 indA4 A4 indT4 T4
    ...
    where A, B, C, D, E are atomic labels, indR, indA, indT are reference
    atom indices, R are bond lengths (in Angstroms), A are bond angles (in
    degrees) and T are dihedral angles (in degrees). For example, E is a
    distance R from atom indR with an E-indR-indA angle of A and an
    E-indR-indA-indT dihedral angle of T. Alternatively, values can be
    assigned to a list of variables after the Z-matrix (preceded by a blank
    line).

    Although the number of atoms is not provided, the unique format of the
    first atom allows multiple geometries to be read without separation
    by a comment line.

    For the time being, vector input is not supported for the
    Z-matrix file format.
    """
    if hascom:
        comment = infile.readline().strip()
    else:
        comment = ''
    data = []
    vlist = dict()
    while True:
        pos = infile.tell()
        line = infile.readline()
        split = line.split()
        if line == '':
            # end-of-file
            break
        elif len(split) == 1 and len(data) > 0:
            # roll back one line before break
            infile.seek(pos)
            break
        elif split == []:
            # blank line before variable assignment
            continue
        elif split[0] in con.sym:
            data.append(split)
        elif split[1] == '=' and len(split) == 3:
            vlist[split[0]] = float(split[2])
        else:
            # assume it's a comment line and roll back
            infile.seek(pos)
            break

    natm = len(data)
    if natm < 1:
        raise ValueError('Geometry not in Z-matrix format.')
    elem = np.array([line[0] for line in data])
    xyz = np.zeros((natm, 3))
    for i in range(natm):
        if i == 0:
            # leave first molecule at origin
            continue
        elif i == 1:
            # move along z-axis by R
            xyz = displace.translate(xyz, _valvar(data[1][2], vlist),
                                     [0, 0, 1], ind=1)
        elif i == 2:
            indR = int(data[2][1]) - 1
            indA = int(data[2][3]) - 1
            xyz[2] = xyz[indR]
            # move from indR towards indA by R
            xyz = displace.translate(xyz, _valvar(data[2][2], vlist),
                                     xyz[indA]-xyz[indR], ind=2)
            # rotate into xz-plane by A
            xyz = displace.rotate(xyz, _valvar(data[2][4], vlist), [0, 1, 0],
                                  ind=2, origin=xyz[indR], units='deg')
        else:
            indR = int(data[i][1]) - 1
            indA = int(data[i][3]) - 1
            indT = int(data[i][5]) - 1
            xyz[i] = xyz[indR]
            # move from indR towards indA by R
            xyz = displace.translate(xyz, _valvar(data[i][2], vlist),
                                     xyz[indA]-xyz[indR], ind=i)
            # rotate about (indT-indA)x(indR-indA) by A
            xyz = displace.rotate(xyz, _valvar(data[i][4], vlist),
                                  np.cross(xyz[indT]-xyz[indA],
                                           xyz[indR]-xyz[indA]),
                                  ind=i, origin=xyz[indR], units='deg')
            # rotate about indR-indA by T
            xyz = displace.rotate(xyz, _valvar(data[i][6], vlist),
                                  xyz[indR]-xyz[indA],
                                  ind=i, origin=xyz[indR], units='deg')

    xyz = displace.centre_mass(elem, xyz) * con.conv(units, 'ang')
    if hasvec:
        vec = np.zeros_like(xyz)
    else:
        vec = None
    return elem, xyz, vec, comment


def read_trajdump(infile, units='bohr', hasvec=False, hascom=False,
                  elem=None, time=None):
    """Reads input file in FMS90/FMSpy TrajDump format

    TrajDump files are in the format:
    T1 X1 Y1 Z1 X2 Y2 ... Vx1 Vy1 Vz1 Vx2 Vy2 ... G Re(A) Im(A) |A| S
    T2 X1 Y1 Z1 X2 Y2 ... Vx1 Vy1 Vz1 Vx2 Vy2 ... G Re(A) Im(A) |A| S
    ...
    where T is the time, Vq are the vectors (momenta) for cartesian
    coordinates q, G is the phase, A is the amplitude and S is the state
    label. The vectors are only read if hasvec = True.

    TrajDump files do not contain atomic labels. If not provided, they are
    set to dummy atoms which may affect calculations involving atomic
    properties. A time should be provided, otherwise the first geometry
    in the file is used.
    """
    if hascom:
        comment = infile.readline().strip()
    else:
        comment = ''
    if time is None:
        rawline = infile.readline().split()
        if rawline == []:
            raise ValueError('empty line provided')
        elif 'Time' in rawline:
            line = np.array(infile.readline().split(), dtype=float)
        else:
            line = np.array(rawline, dtype=float)
    else:
        alldata = np.array([line.split() for line in infile.readlines()])
        alldata = alldata[[dat[0] != '#' for dat in alldata[:,0]]].astype(float)
        line = alldata[np.abs(alldata[:,0] - t) < 1e-6][0]
    natm = len(line) // 6 - 1
    if elem is None:
        elem = np.array(['X'] * natm)
    xyz = line[1:3*natm+1].reshape(natm, 3) * con.conv(units,'ang')
    if hasvec:
        vec = line[3*natm+1:6*natm+1].reshape(natm, 3)
    else:
        vec = None
    return elem, xyz, vec, comment


def read_auto(infile, hascom=False, **kwargs):
    """Reads a molecular geometry file and determines the format."""
    pos = infile.tell()
    contents = infile.readlines()
    infile.seek(pos)
    nlines = min(len(contents), 4)
    fmt = []
    for i in range(nlines):
        line = contents[i].split()
        fmt.append(''.join([_get_type(l) for l in line]))

    if nlines == 0:
        raise ValueError('end of file')
    elif nlines == 1:
        if hascom:
            raise IOError('cannot have comment with single line file')
        else:
            if fmt[0] == 's':
                return read_zmt(infile, **kwargs)
            elif fmt[0].replace('i', 'f') == 'sfffff':
                return read_col(infile, **kwargs)
            elif 'ffffffffffff' in fmt[0].replace('i', 'f'):
                return read_trajdump(infile, **kwargs)
            else:
                raise IOError('single line input in unrecognized format')
    elif nlines == 2 and hascom:
        if fmt[1] == 's':
            return read_zmt(infile, **kwargs)
        elif fmt[1].replace('i', 'f') == 'sfffff':
            return read_col(infile, **kwargs)
        elif 'ffffffffffff' in fmt[1].replace('i', 'f'):
            return read_trajdump(infile, **kwargs)
        else:
            raise IOError('single line input in unrecognized format')
    else:
        if hascom:
            if fmt[1] == 's' and fmt[2] in ['sis', 'sif', 'sii']:
                return read_zmt(infile, **kwargs)
            elif [f.replace('i', 'f') for f in fmt[1:3]] == ['sfffff', 'sfffff']:
                return read_col(infile, **kwargs)
        else:
            if fmt[0] == 's' and fmt[1] in ['sis', 'sif', 'sii']:
                return read_zmt(infile, **kwargs)
            elif [f.replace('i', 'f') for f in fmt[:2]] == ['sfffff', 'sfffff']:
                return read_col(infile, **kwargs)

        if ('ffffffffffff' in fmt[0].replace('i', 'f') or
            'ffffffffffff' in fmt[1].replace('i', 'f')):
            return read_trajdump(infile, **kwargs)
        elif nlines > 2:
            if fmt[0] == 'i':
                return read_xyz(infile, **kwargs)
            elif fmt[1] == 'i':
                return read_gdat(infile, **kwargs)
        else:
            raise IOError('unrecognized file format')


def _get_type(s):
    """Reads a string to see if it can be converted into int or float."""
    try:
        float(s)
        if '.' not in s:
            return 'i'
        else:
            return 'f'
    except ValueError:
        return 's'


def _valvar(unk, vardict):
    """Determines if an unknown string is a value or a dict variable."""
    try:
        return float(unk)
    except ValueError:
        if unk in vardict:
            return vardict[unk]
        else:
            raise KeyError('\'{}\' not found in variable list'.format(unk))


def write_xyz(outfile, elem, xyz, vec=None, comment='', units='ang'):
    """Writes geometry to an output file in XYZ format."""
    natm = len(elem)
    write_xyz = xyz * con.conv('ang', units)
    outfile.write(' {}\n{}\n'.format(natm, comment))
    if vec is None:
        for atm, xyzi in zip(elem, write_xyz):
            outfile.write('{:4s}{:12.6f}{:12.6f}{:12.6f}\n'.format(atm, *xyzi))
    else:
        for atm, xyzi, pxyzi in zip(elem, write_xyz, vec):
            outfile.write('{:4s}{:12.6f}{:12.6f}{:12.6f}'.format(atm, *xyzi) +
                          '{:12.6f}{:12.6f}{:12.6f}\n'.format(*pxyzi))


def write_col(outfile, elem, xyz, vec=None, comment='', units='bohr'):
    """Writes geometry to an output file in COLUMBUS format.

    For the time being, vector output is not supported for the
    COLUMBUS file format.
    """
    write_xyz = xyz * con.conv('ang', units)
    if comment != '':
        outfile.write(comment + '\n')
    for atm, (x, y, z) in zip(elem, write_xyz):
        outfile.write(' {:<2s}{:7.1f}{:14.8f}{:14.8f}{:14.8f}{:14.8f}'
                      '\n'.format(atm, con.get_num(atm), x, y, z,
                                  con.get_mass(atm)))


def write_gdat(outfile, elem, xyz, vec=None, comment='', units='bohr'):
    """Writes geometry to an output file in Geometry.dat format."""
    natm = len(elem)
    write_xyz = xyz * con.conv('ang', units)
    outfile.write('{}\n{}\n'.format(comment, natm))
    for atm, xyzi in zip(elem, write_xyz):
        outfile.write('{:<2s}{:18.8E}{:18.8E}{:18.8E}\n'.format(atm, *xyzi))
    if vec is None:
        for line in range(natm):
            outfile.write(' {:18.8E}{:18.8E}{:18.8E}\n'.format(0, 0, 0))
    else:
        for pxyzi in vec:
            outfile.write(' {:18.8E}{:18.8E}{:18.8E}\n'.format(*pxyzi))


def write_zmt(outfile, elem, xyz, vec=None, comment='', units='ang'):
    """Writes geometry to an output file in Z-matrix format.

    TODO: At present, each atom uses the previous atoms in order as
    references. This could be made 'smarter' using the bonding module.

    For the time being, vector output is not supported for the
    Z-matrix file format.
    """
    natm = len(elem)
    if comment != '':
        outfile.write(comment + '\n')
    for i in range(natm):
        if i == 0:
            # first element has just the symbol
            outfile.write('{:<2}\n'.format(elem[0]))
        elif i == 1:
            # second element has symbol, index, bond length
            outfile.write('{:<2}{:3d}{:12.6f}'
                          '\n'.format(elem[1], 1, measure.stre(xyz, 0, 1,
                                                               units=units)))
        elif i == 2:
            # third element has symbol, index, bond length, index, bond angle
            outfile.write('{:<2}{:3d}{:12.6f}{:3d}{:12.6f}'
                          '\n'.format(elem[2], 2, measure.stre(xyz, 1, 2,
                                                               units=units),
                                      1, measure.bend(xyz, 0, 1, 2,
                                                      units='deg')))
        else:
            # all other elements have symbol, index, bond length, index,
            # bond angle, index, dihedral angle
            outfile.write('{:<2}{:3d}{:12.6f}{:3d}{:12.6f}{:3d}{:12.6f}'
                          '\n'.format(elem[i], i, measure.stre(xyz, i-1, i,
                                                               units=units),
                                      i-1, measure.bend(xyz, i-2, i-1, i,
                                                        units='deg'),
                                      i-2, measure.tors(xyz, i-3, i-2, i-1, i,
                                                        units='deg')))


def write_zmtvar(outfile, elem, xyz, vec=None, comment='', units='ang'):
    """Writes geometry to an output file in Z-matrix format with
    variable assignments.

    For the time being, vector output is not supported for the
    Z-matrix file format.
    """
    natm = len(elem)
    if comment != '':
        outfile.write(comment + '\n')
    vlist = dict()
    for i in range(natm):
        if i == 0:
            # first element has just the symbol
            outfile.write('{:<2}\n'.format(elem[0]))
        elif i == 1:
            # second element has symbol, index, bond length
            outfile.write('{:<2}{:3d}  R{:<2d}'
                          '\n'.format(elem[1], 1, 1))
            vlist['R1'] = measure.stre(xyz, 0, 1, units=units)
        elif i == 2:
            # third element has symbol, index, bond length, index, bond angle
            outfile.write('{:<2}{:3d}  R{:<2d} {:3d}  A{:<2d}'
                          '\n'.format(elem[2], 2, 2, 1, 1))
            vlist['R2'] = measure.stre(xyz, 1, 2, units=units)
            vlist['A1'] = measure.bend(xyz, 0, 1, 2, units='deg')
        else:
            # all other elements have symbol, index, bond length, index,
            # bond angle, index, dihedral angle
            outfile.write('{:<2}{:3d}  R{:<2d} {:3d}  A{:<2d} '
                          '{:3d}  T{:<2d}'
                          '\n'.format(elem[i], i, i, i-1, i-1, i-2, i-2))
            vlist['R'+str(i)] = measure.stre(xyz, i-1, i, units=units)
            vlist['A'+str(i-1)] = measure.bend(xyz, i-2, i-1, i, units='deg')
            vlist['T'+str(i-2)] = measure.tors(xyz, i-3, i-2, i-1, i,
                                               units='deg')
    outfile.write('\n')
    for key, val in vlist.items():
        outfile.write('{:4s} = {:14.8f}\n'.format(key, val))


def write_auto(outfile, elem, xyz, **kwargs):
    """Writes geometry to an output file based on the filename extension.

    Extensions are not case sensitive. If the extension is not recognized,
    the default format is XYZ.
    """
    fname = outfile.name.lower()
    ext = fname.split('.')[-1]
    if ext in ['col', 'columbus']:
        write_col(outfile, elem, xyz, **kwargs)
    elif ext == 'dat':
        write_gdat(outfile, elem, xyz, **kwargs)
    elif ext in ['zmt', 'zmat', 'zmatrix']:
        write_zmt(outfile, elem, xyz, **kwargs)
    elif ext in ['zmtvar', 'zmatvar']:
        write_zmtvar(outfile, elem, xyz, **kwargs)
    else:
        write_xyz(outfile, elem, xyz, **kwargs)


def convert(infname, outfname, infmt='auto', outfmt='auto',
            inunits=None, outunits=None, hasvec=False, hascom=False):
    """Reads a file in format infmt and writes to a file in format
    outfmt.

    Input (and output) may have multiple geometries. Z-matrix index
    ordering is not conserved.
    """
    if inunits is None:
        inkw = dict(hasvec=hasvec, hascom=hascom)
    else:
        inkw = dict(hasvec=hasvec, hascom=hascom, units=inunits)
    if outunits is None:
        outkw = dict()
    else:
        outkw = dict(units=outunits)

    read_func = globals()['read_' + infmt]
    write_func = globals()['write_' + outfmt]
    with open(infname, 'r') as infile, open(outfname, 'w') as outfile:
        while True:
            try:
                elem, xyz, vec, comment = read_func(infile, **inkw)
                if hasvec:
                    outkw.update(vec = vec)
                if hascom:
                    outkw.update(comment = comment)
                write_func(outfile, elem, xyz, **outkw)
            except ValueError:
                break


def convert_trajdump(infname, outfname, outfmt='auto', elem=None, times=None):
    """Reads an FMS TrajDump file and writes to a file in format outfmt.

    An element list should be provided, otherwise dummy atoms (X) will be
    assumed. A time or list of times can be specified. Otherwise, the full
    trajectory will be read.

    Note: This is the same as using infmt='trajdump' with convert, except
    for the option to add atomic labels and the automatic comment line.
    """
    write_func = globals()['write_' + outfmt]
    with open(infname, 'r') as infile, open(outfname, 'w') as outfile:
        infile.readline()
        alldata = np.array([line.split() for line in infile.readlines()])
        alldata = alldata[[dat[0] != '#' for dat in alldata[:,0]]].astype(float)
        if times is None:
            numdata = np.copy(alldata)
        else:
            times = np.atleast_1d(times)
            numdata = np.empty((len(times), len(alldata[1])))
            for i, t in enumerate(times):
                numdata[i] = alldata[np.abs(alldata[:,0] - t) < 1e-6]
        for line in numdata:
            natm = len(line) // 6 - 1
            if elem is None:
                elem = ['X'] * natm
            ti = line[0]
            xyz = line[1:3*natm+1].reshape(natm, 3) * con.conv('bohr','ang')
            pop = line[-2]
            write_func(outfile, elem, xyz,
                       comment='t = {:.2f}, pop = {:.4f}'.format(ti, pop))