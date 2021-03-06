"""
Example inputs and expected results for different tests
"""
import numpy as np


class Geometries:
    """
    Library of geometries for test routines
    """
    he = (np.array('He', dtype='<U2'), np.zeros(3))

    h2 = (np.array(['H', 'H'], dtype='<U2'),
          np.array([[ 0.000000,  0.000000,  0.370000],
                    [ 0.000000,  0.000000, -0.370000]]))

    ch4 = (np.array(['C', 'H', 'H', 'H', 'H'], dtype='<U2'),
           np.array([[ 0.000000,  0.000000,  0.000000],
                     [ 0.629118,  0.629118,  0.629118],
                     [-0.629118, -0.629118,  0.629118],
                     [ 0.629118, -0.629118, -0.629118],
                     [-0.629118,  0.629118, -0.629118]]))

    ch4_zmt = (np.array(['C', 'H', 'H', 'H', 'H'], dtype='<U2'),
               np.array([[ 0.000000,  0.000000,  0.000000],
                         [ 0.000000,  0.000000,  1.089664],
                         [-1.027345,  0.000000, -0.363221],
                         [ 0.513673, -0.889707, -0.363221],
                         [ 0.513673,  0.889707, -0.363221]]))

    c2h4 = (np.array(['C', 'C', 'H', 'H', 'H', 'H'], dtype='<U2'),
            np.array([[ 0.000000,  0.000000,  0.667480],
                      [ 0.000000,  0.000000, -0.667480],
                      [ 0.000000,  0.922832,  1.237695],
                      [ 0.000000, -0.922832,  1.237695],
                      [ 0.000000,  0.922832, -1.237695],
                      [ 0.000000, -0.922832, -1.237695]]))

    c2h4_ms = (np.array(['C', 'C', 'H', 'H', 'H', 'H'], dtype='<U2'),
               np.array([[ 0.000000,  0.000000,  0.667480],
                         [ 0.000000,  0.000000, -0.667480],
                         [-0.107486,  0.842005,  1.342934],
                         [ 0.950491, -0.522308,  0.690394],
                         [ 0.000000,  0.922832, -1.237695],
                         [ 0.000000, -0.922832, -1.237695]]))

    c3h8 = (np.array(['C', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
                     dtype='<U2'),
            np.array([[ 0.000000,  0.000000,  0.578619],
                      [ 0.000000,  1.266857, -0.269285],
                      [ 0.000000, -1.266857, -0.269285],
                      [-0.876898,  0.000000,  1.235614],
                      [ 0.876898,  0.000000,  1.235614],
                      [ 0.000000,  2.166150,  0.352968],
                      [ 0.000000, -2.166150,  0.352968],
                      [ 0.883619,  1.304234, -0.913505],
                      [-0.883619,  1.304234, -0.913505],
                      [-0.883619, -1.304234, -0.913505],
                      [ 0.883619, -1.304234, -0.913505]]))

    c2h3f = (np.array(['C', 'C', 'F', 'H', 'H', 'H'], dtype='<U2'),
             np.array([[ 0.00000000,  0.00000000,  0.66748000],
                       [ 0.00000000,  0.00000000, -0.66748000],
                       [ 0.00000000,  1.15695604,  1.38235951],
                       [ 0.00000000, -0.92283200,  1.23769500],
                       [ 0.00000000,  0.92283200, -1.23769500],
                       [ 0.00000000, -0.92283200, -1.23769500]]))

    c2h3me = (np.array(['C', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H'],
                       dtype='<U2'),
              np.array([[ 0.00000000,  0.00000000,  0.66748000],
                        [ 0.00000000,  0.00000000, -0.66748000],
                        [ 0.00000000,  1.22501228,  1.42441125],
                        [ 0.88600000,  1.81433276,  1.18787083],
                        [-0.88600000,  1.81433276,  1.18787083],
                        [ 0.00000000,  1.00799073,  2.49284919],
                        [ 0.00000000, -0.92283200,  1.23769500],
                        [ 0.00000000,  0.92283200, -1.23769500],
                        [ 0.00000000, -0.92283200, -1.23769500]]))

    c2h3me_ax = (np.array(['C', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H'],
                          dtype='<U2'),
                 np.array([[ 0.00000000,  0.00000000,  0.66748000],
                           [ 0.00000000,  0.00000000, -0.66748000],
                           [ 0.00000000,  1.22501228,  1.42441125],
                           [-0.42313789,  0.22682954,  1.31113487],
                           [ 0.59992678,  1.24989422,  2.33419954],
                           [-0.81613949,  1.9409233 ,  1.52463972],
                           [ 0.00000000, -0.92283200,  1.23769500],
                           [ 0.00000000,  0.92283200, -1.23769500],
                           [ 0.00000000, -0.92283200, -1.23769500]]))

    c4h4 = (np.array(['C', 'C', 'C', 'C', 'H', 'H', 'H', 'H'], dtype='<U2'),
            np.array([[ 0.710000,  0.710000,  0.000000],
                      [ 0.710000, -0.710000,  0.000000],
                      [-0.710000,  0.710000,  0.000000],
                      [-0.710000, -0.710000,  0.000000],
                      [ 1.473675,  1.473675,  0.000000],
                      [ 1.473675, -1.473675,  0.000000],
                      [-1.473675,  1.473675,  0.000000],
                      [-1.473675, -1.473675,  0.000000]]))

    p4 = (np.array(['P', 'P', 'P', 'P'], dtype='<U2'),
          np.array([[-0.885000, -0.511000, -0.361300],
                    [ 0.885000, -0.511000, -0.361300],
                    [ 0.000000,  1.021900, -0.361300],
                    [ 0.000000,  0.000000,  1.083900]]))

    ch2f2 = (np.array(['C', 'H', 'H', 'F', 'F'], dtype='<U2'),
             np.array([[ 0.000000,  0.000000,  0.000000],
                       [ 0.000000,  0.000000,  1.000000],
                       [ 0.000000,  1.000000,  0.000000],
                       [ 1.000000,  0.000000,  0.000000],
                       [-1.000000,  0.000000,  0.000000]]),
             np.array([[ 0.000000,  0.000000,  0.000000],
                       [ 1.020000, -1.020000,  0.000000],
                       [ 1.020000,  1.020000,  0.000000],
                       [-1.020000,  1.020000,  0.000000],
                       [ 0.000000,  0.000000,  1.020000]]),
             np.array([[ 0.000000,  0.000000,  0.000000],
                       [ 0.000000,  0.000000, -1.010000],
                       [ 0.000000,  0.990000,  0.000000],
                       [ 1.000000,  0.000000,  0.000000],
                       [-1.000000,  0.000000,  0.000000]]),
             np.array([[ 0.000000,  0.000000,  0.000000],
                       [ 1.000000,  0.000000,  0.000000],
                       [ 0.000000,  1.000000,  0.000000],
                       [ 0.000000,  0.000000,  0.980000],
                       [-1.020000,  0.000000,  0.000000]]),
             np.array([[ 0.000000,  0.000000,  0.000000],
                       [ 0.000000, -1.000000,  0.000000],
                       [ 0.000000,  0.000000, -1.000000],
                       [ 0.000000,  1.000000,  0.000000],
                       [ 1.000000, -1.000000,  0.000000]]))


class Files:
    """
    Library of input/output file formats for test routines.
    """
    xyz_novec = (' 5\n' +
                 'comment line\n' +
                 'C       0.000000    0.000000    0.000000\n' +
                 'H       0.629118    0.629118    0.629118\n' +
                 'H      -0.629118   -0.629118    0.629118\n' +
                 'H       0.629118   -0.629118   -0.629118\n' +
                 'H      -0.629118    0.629118   -0.629118\n')

    xyz_bohr = (' 5\n' +
                'comment line\n' +
                'C       0.000000    0.000000    0.000000\n' +
                'H       1.188861    1.188861    1.188861\n' +
                'H      -1.188861   -1.188861    1.188861\n' +
                'H       1.188861   -1.188861   -1.188861\n' +
                'H      -1.188861    1.188861   -1.188861\n')

    xyz_vec = (' 5\n' +
               'comment line\n' +
               'C       0.000000    0.000000    0.000000' +
               '    1.000000    1.000000    1.000000\n' +
               'H       0.629118    0.629118    0.629118' +
               '    1.000000    1.000000    1.000000\n' +
               'H      -0.629118   -0.629118    0.629118' +
               '    1.000000    1.000000    1.000000\n' +
               'H       0.629118   -0.629118   -0.629118' +
               '    1.000000    1.000000    1.000000\n' +
               'H      -0.629118    0.629118   -0.629118' +
               '    1.000000    1.000000    1.000000\n')

    col_nocom = (' C     6.0    0.00000000    0.00000000    0.00000000' +
                 '   12.00000000\n' +
                 ' H     1.0    1.18886072    1.18886072    1.18886072' +
                 '    1.00782504\n' +
                 ' H     1.0   -1.18886072   -1.18886072    1.18886072' +
                 '    1.00782504\n' +
                 ' H     1.0    1.18886072   -1.18886072   -1.18886072' +
                 '    1.00782504\n' +
                 ' H     1.0   -1.18886072    1.18886072   -1.18886072' +
                 '    1.00782504\n')

    col_com = 'comment line\n' + col_nocom

    gdat_bohr = ('comment line\n' +
                 '5\n' +
                 'C     0.00000000E+00    0.00000000E+00    0.00000000E+00\n' +
                 'H     1.18886072E+00    1.18886072E+00    1.18886072E+00\n' +
                 'H    -1.18886072E+00   -1.18886072E+00    1.18886072E+00\n' +
                 'H     1.18886072E+00   -1.18886072E+00   -1.18886072E+00\n' +
                 'H    -1.18886072E+00    1.18886072E+00   -1.18886072E+00\n' +
                 '     1.00000000E+00    1.00000000E+00    1.00000000E+00\n' +
                 '     1.00000000E+00    1.00000000E+00    1.00000000E+00\n' +
                 '     1.00000000E+00    1.00000000E+00    1.00000000E+00\n' +
                 '     1.00000000E+00    1.00000000E+00    1.00000000E+00\n' +
                 '     1.00000000E+00    1.00000000E+00    1.00000000E+00\n')

    gdat_ang = ('\n' +
                '5\n' +
                'C     0.00000000E+00    0.00000000E+00    0.00000000E+00\n' +
                'H     6.29118000E-01    6.29118000E-01    6.29118000E-01\n' +
                'H    -6.29118000E-01   -6.29118000E-01    6.29118000E-01\n' +
                'H     6.29118000E-01   -6.29118000E-01   -6.29118000E-01\n' +
                'H    -6.29118000E-01    6.29118000E-01   -6.29118000E-01\n' +
                '     1.00000000E+00    1.00000000E+00    1.00000000E+00\n' +
                '     1.00000000E+00    1.00000000E+00    1.00000000E+00\n' +
                '     1.00000000E+00    1.00000000E+00    1.00000000E+00\n' +
                '     1.00000000E+00    1.00000000E+00    1.00000000E+00\n' +
                '     1.00000000E+00    1.00000000E+00    1.00000000E+00\n')

    zmt_nocom = ('C\n' +
                 'H   1    1.089664\n' +
                 'H   2    1.779414  1   35.264390\n' +
                 'H   3    1.779414  2   60.000000  1   35.264390\n' +
                 'H   4    1.779414  3   60.000000  2  -70.528779\n')

    zmt_com = 'comment line\n' + zmt_nocom

    zmtvar_nocom = ('C\n' +
                    'H   1  R1\n' +
                    'H   2  R2    1  A1\n' +
                    'H   3  R3    2  A2    1  T1\n' +
                    'H   4  R4    3  A3    2  T2\n' +
                    '\n' +
                    'R1   =     1.08966434\n' +
                    'R2   =     1.77941442\n' +
                    'A1   =    35.26438968\n' +
                    'R3   =     1.77941442\n' +
                    'A2   =    60.00000000\n' +
                    'T1   =    35.26438968\n' +
                    'R4   =     1.77941442\n' +
                    'A3   =    60.00000000\n' +
                    'T2   =   -70.52877937\n')

    zmtvar_com = 'comment line\n' + zmtvar_nocom

    traj_nocom = ('      0.00    0.0000    0.0000    0.0000    1.1889' +
                  '    1.1889    1.1889   -1.1889   -1.1889    1.1889' +
                  '    1.1889   -1.1889   -1.1889   -1.1889    1.1889' +
                  '   -1.1889    1.0000    1.0000    1.0000    1.0000' +
                  '    1.0000    1.0000    1.0000    1.0000    1.0000' +
                  '    1.0000    1.0000    1.0000    1.0000    1.0000' +
                  '    1.0000    0.0000    0.4000    0.3000    0.2500' +
                  '    2.0000\n')

    traj_time = ('    # Time    pos.1x    pos.1y    pos.1z    pos.2x' +
                 '    pos.2y    pos.2z    pos.3x    pos.3y    pos.3z' +
                 '    pos.4x    pos.4y    pos.4z    pos.5x    pos.5y' +
                 '    pos.5z    mom.1x    mom.1y    mom.1z    mom.2x' +
                 '    mom.2y    mom.2z    mom.3x    mom.3y    mom.3z' +
                 '    mom.4x    mom.4y    mom.4z    mom.5x    mom.5y' +
                 '    mom.5z     Phase   AmpReal   AmpImag   AmpNorm' +
                 '   StateID\n' +
                 traj_nocom + traj_nocom.replace(' 0.00 ', ' 1.00 '))

    traj_com = 'comment line\n' + traj_nocom

    @staticmethod
    def tmpf(tmpdir, contents, fname='tmp.geom'):
        """Writes a temporary file to test reading."""
        fout = tmpdir.join(fname)
        fout.write(contents)
        return fout.open()
