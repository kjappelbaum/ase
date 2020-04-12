"""Module to read and write atoms in xtl file format for the prismatic and
computem software.

See https://prism-em.com/docs-inputs for an example of this format and the
documentation of prismatic.

See https://sourceforge.net/projects/computem/ for the source code of the
computem software.
"""

import numpy as np

from ase.atoms import symbols2numbers


def _check_numpy_version():
    # This writer doesn't support numpy < 1.14 because of the issue:
    # https://github.com/numpy/numpy/issues/10018
    from distutils.version import LooseVersion
    if LooseVersion(np.__version__) < LooseVersion("1.14"):
        raise NotImplementedError("Writing this format needs numpy >= 1.14.")


def read_prismatic(filename):
    """Import prismatic and computem xyz input file.

    Reads cell, atom positions, occupancy and Debye Waller factor
    """
    _check_numpy_version()

    from ase import Atoms
    from ase.geometry import cellpar_to_cell

    if isinstance(filename, str):
        f = open(filename)
    else:  # Assume it's a file-like object
        f = filename

    # Read comment:
    f.readline()

    # Read unit cell parameters:
    cellpar = [float(i) for i in f.readline().strip().split()]

    # Read all data at once
    # Use genfromtxt instead of loadtxt to skip last line
    read_data = np.genfromtxt(fname=filename, skip_footer=1)


    atoms = Atoms(symbols=read_data[:, 0],
                  positions=read_data[:, 1:4],
                  cell=cellpar_to_cell(cellpar),
                  )
    atoms.set_array('occupancy', read_data[:, 4])
    atoms.set_array('debye_waller_factor', read_data[:, 5])

    return atoms


class XYZPrismaticWriter:
    """Write xyz file for prismatic and computem.

    Parameters:

    atoms: Atoms object

    DW: float or dictionary of float with atom type as key
        Debye-Waller factor of each atoms.

    comment: str (optional)
        Comments to be written in the first line of the file. If not
        provided, write the total number of atoms and the chemical formula.

    """

    def __init__(self, atoms, DW=None, comments=None):
        cell = atoms.get_cell()
        if not cell.orthorhombic:
            raise ValueError('To export to this format, the cell needs to be '
                             'orthorhombic.')
        if (cell.diagonal() ==  0).any():
            raise ValueError('To export to this format, the cell size needs '
                             'to be set: current cell is {}.'.format(cell))
        self.atoms = atoms.copy()
        self.atom_types = set(atoms.get_chemical_symbols())
        self.comments = comments

        self.occupancy = self._get_occupancy()
        self.DW = self._get_DW(DW)

    def _get_occupancy(self):
        if 'occupancy' in self.atoms.arrays:
            occupancy = self.atoms.get_array('occupancy', copy=False)
        else:
            occupancy = np.ones_like(self.atoms.numbers)

        return occupancy

    def _get_DW(self, DW):
        if np.isscalar(DW):
            DW = np.ones_like(self.atoms.numbers) * DW
        elif isinstance(DW, dict):
            self._check_key_dictionary(DW, 'DW')
            # Get the arrays of DW from mapping the DW defined by symbol
            DW = {symbols2numbers(k)[0]:v for k, v in DW.items()}
            DW = np.vectorize(DW.get)(self.atoms.numbers)
        else:
            # If
            for name in ['DW', 'debye_waller_factor']:
                if name in self.atoms.arrays:
                    DW = self.atoms.get_array(name)

        if DW is None:
            raise ValueError('Missing Debye-Waller factors. It can be '
                             'provided as a dictionary with symbols as key or '
                             'can be set for each atom by using the '
                             '`set_array("debye_waller_factor", values)` of '
                             'the `Atoms` object.')

        return DW


    def _check_key_dictionary(self, d, dict_name):
        # Check if we have enough key
        for key in self.atom_types:
            if key not in d:
                raise ValueError('Missing the {} key in the `{}` dictionary.'
                                 ''.format(key, dict_name))

    def _get_file_header(self):
        # 1st line: comment line
        if self.comments is None:
            s = "{0} atoms with chemical formula: {1}.".format(
                len(self.atoms),
                self.atoms.get_chemical_formula())
        else:
            s = self.comments

        s = s.strip()
        s += " generated by the ase library.\n"
        # 2nd line: lattice parameter
        s += "{} {} {}".format(
            *self.atoms.get_cell_lengths_and_angles()[:3])

        return s

    def write_to_file(self, f):
        data_array = np.vstack((self.atoms.numbers,
                                self.atoms.positions.T,
                                self.occupancy,
                                self.DW)
                               ).T

        np.savetxt(fname=f,
                   X=data_array,
                   fmt='%.6g',
                   header=self._get_file_header(),
                   newline='\n',
                   footer='-1',
                   comments=''
                   )


def write_prismatic(filename, *args, **kwargs):

    _check_numpy_version()

    writer = XYZPrismaticWriter(*args, **kwargs)
    writer.write_to_file(filename)
