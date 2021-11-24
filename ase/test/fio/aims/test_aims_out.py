# flake8: noqa
import numpy as np
from ase.io import read
from ase.io.aims import read_aims_results
from numpy.linalg import norm
from pathlib import Path

parent = Path(__file__).parent


def test_parse_socketio(testdir):
    traj = read(parent / "aims_out_files/socket.out", ":", format="aims-output")
    assert len(traj) == 6
    p0 = [[0.0, 0.0, 0.0], [0.9584, 0.0, 0.0], [-0.24, 0.9279, 0.0]]
    p1 = [
        [-0.00044436, 0.00021651, 0.00068957],
        [0.96112981, -0.00029923, 0.00096836],
        [-0.24091781, 0.93010946, 0.00061317],
    ]
    p_end = [
        [-0.00156048, -0.00072446, 0.00045281],
        [0.98615072, -0.00962614, -0.00053732],
        [-0.25646779, 0.95117586, 0.00820183],
    ]
    assert np.allclose(traj[0].get_positions(), p0)
    assert np.allclose(traj[1].get_positions(), p1)
    assert np.allclose(traj[-1].get_positions(), p_end)

    f0 = [
        [-0.481289284665163e00, -0.615051370384412e00, 0.811297123282653e-27],
        [0.762033585727896e00, -0.942008578636939e-01, -0.973556547939183e-27],
        [-0.280744301062733e00, 0.709252228248106e00, -0.649037698626122e-27],
    ]
    f1 = [
        [-0.346210275412861e00, -0.520615919604426e00, -0.966369462150621e-04],
        [0.587866333819113e00, -0.830442530429637e-01, 0.171037714240380e-03],
        [-0.241656058406252e00, 0.603660172647390e00, -0.744007680253175e-04],
    ]
    f_end = [
        [0.492882061544499e00, 0.499117230159087e00, 0.347959116743205e-02],
        [-0.724281788245024e00, 0.800633239635954e-01, 0.130633777464187e-02],
        [0.231399726700525e00, -0.579180554122683e00, -0.478592894207392e-02],
    ]
    assert np.allclose(traj[0].get_forces(), f0)
    assert np.allclose(traj[1].get_forces(), f1)
    assert np.allclose(traj[-1].get_forces(), f_end)


def test_parse_md(testdir):
    traj = read(parent / "aims_out_files/md.out", ":", format="aims-output")
    assert len(traj) == 5
    p0 = [[0.0, 0.0, 0.0], [0.9584, 0.0, 0.0], [-0.24, 0.9279, 0.0]]
    p1 = [
        [0.00247722, -0.00200215, 0.00000000],
        [0.93156204, -0.00330135, 0.00000000],
        [-0.25248383, 0.96298223, 0.00000000],
    ]
    p_end = [
        [-0.00044308, -0.00190646, 0.00000000],
        [0.98936333, -0.01341746, -0.00000000],
        [-0.26393022, 0.97157934, 0.00000000],
    ]
    assert np.allclose(traj[0].get_positions(), p0)
    assert np.allclose(traj[1].get_positions(), p1)
    assert np.allclose(traj[-1].get_positions(), p_end)

    f0 = [
        [-0.481289284665163e00, -0.615051370384412e00, 0.811297123282653e-27],
        [0.762033585727896e00, -0.942008578636939e-01, -0.973556547939183e-27],
        [-0.280744301062733e00, 0.709252228248106e00, -0.649037698626122e-27],
    ]
    f1 = [
        [-0.284519402890037e01, 0.121286349030924e01, 0.691733365155783e-17],
        [0.257911758656866e01, -0.471469245294899e-01, -0.730166238143266e-18],
        [0.266076442331705e00, -0.116571656577975e01, -0.618716741081841e-17],
    ]
    f_end = [
        [0.266848800470869e00, 0.137113486710510e01, 0.717235335588107e-17],
        [-0.812308728045051e00, 0.142880785873554e00, 0.874856850626564e-18],
        [0.545459927574182e00, -0.151401565297866e01, -0.804721020748119e-17],
    ]
    assert np.allclose(traj[0].get_forces(), f0)
    assert np.allclose(traj[1].get_forces(), f1)
    assert np.allclose(traj[-1].get_forces(), f_end)


def test_parse_relax(testdir):
    traj = read(parent / "aims_out_files/relax.out", ":", format="aims-output")
    assert len(traj) == 4
    p0 = [[0.0, 0.0, 0.0], [0.9584, 0.0, 0.0], [-0.24, 0.9279, 0.0]]
    p_end = [
        [-0.00191785, -0.00243279, -0.00000000],
        [0.97071531, -0.00756333, 0.00000000],
        [-0.25039746, 0.93789612, -0.00000000],
    ]
    assert np.allclose(traj[0].get_positions(), p0)
    assert np.allclose(traj[-1].get_positions(), p_end)

    f0 = [
        [-0.481289284665163e00, -0.615051370384412e00, 0.811297123282653e-27],
        [0.762033585727896e00, -0.942008578636939e-01, -0.811297123282653e-28],
        [-0.280744301062733e00, 0.709252228248106e00, -0.324518849313061e-27],
    ]
    f_end = [
        [0.502371358893591e-03, 0.518627680984070e-03, 0.324518849313061e-27],
        [-0.108826759330217e-03, -0.408128913725760e-03, -0.194711309587837e-26],
        [-0.393544599563376e-03, -0.110498767258316e-03, -0.973556547939183e-27],
    ]
    assert np.allclose(traj[0].get_forces(), f0)
    assert np.allclose(traj[-1].get_forces(), f_end)


def test_parse_singlepoint(testdir):
    atoms = read(parent / "aims_out_files/singlepoint.out", format="aims-output")
    p0 = [[0.0, 0.0, 0.0], [0.9584, 0.0, 0.0], [-0.24, 0.9279, 0.0]]
    assert np.allclose(atoms.get_positions(), p0)

    f0 = [
        [-0.481289284665163e00, -0.615051370384412e00, 0.811297123282653e-27],
        [0.762033585727896e00, -0.942008578636939e-01, -0.811297123282653e-28],
        [-0.280744301062733e00, 0.709252228248106e00, -0.324518849313061e-27],
    ]
    assert np.allclose(atoms.get_forces(), f0)

    results = read_aims_results(parent / "aims_out_files/singlepoint.out")
    assert np.allclose(results["forces"], f0)
    assert np.abs(results["energy"] + 2.06777440861977e03) < 1e-15
