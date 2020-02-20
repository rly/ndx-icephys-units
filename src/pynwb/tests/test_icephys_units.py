import numpy as np

from pynwb.device import Device
from pynwb.icephys import IntracellularElectrode
from pynwb.testing import TestCase, AcquisitionH5IOMixin

from ndx_icephys_units import ICEphysUnits


class TestICEphysUnits(TestCase):
    def test_init(self):
        ut = ICEphysUnits()
        self.assertEqual(ut.name, 'ICEphysUnits')
        self.assertFalse(ut.columns)

    def _init_units(self):
        ut = ICEphysUnits()
        ut.add_unit(spike_times=[0., 1., 2.])
        ut.add_unit(spike_times=[3., 4., 5.])
        return ut

    def test_add_spike_times(self):
        ut = self._init_units()
        self.assertEqual(ut.id.data, [0., 1.])
        self.assertEqual(ut['spike_times'].target.data, [0., 1., 2., 3., 4., 5.])
        self.assertEqual(ut['spike_times'].data, [3., 6.])
        self.assertEqual(ut['spike_times'][0], [0., 1., 2.])
        self.assertEqual(ut['spike_times'][1], [3., 4., 5.])

    def test_get_spike_times(self):
        ut = self._init_units()
        self.assertTrue(all(ut.get_unit_spike_times(0) == np.array([0., 1., 2.])))
        self.assertTrue(all(ut.get_unit_spike_times(1) == np.array([3., 4., 5.])))

    def test_get_spike_times_interval(self):
        ut = self._init_units()
        np.testing.assert_array_equal(ut.get_unit_spike_times(0, (.5, 3)), [1, 2])
        np.testing.assert_array_equal(ut.get_unit_spike_times(0, (-.5, 1.1)), [0, 1])

    def test_get_spike_times_multi(self):
        ut = self._init_units()
        np.testing.assert_array_equal(ut.get_unit_spike_times((0, 1)), [[0, 1, 2], [3, 4, 5]])

    def test_get_spike_times_multi_interval(self):
        ut = self._init_units()
        np.testing.assert_array_equal(ut.get_unit_spike_times((0, 1), (1.5, 3.5)), [[2], [3]])

    def test_times(self):
        ut = self._init_units()
        self.assertTrue(all(ut['spike_times'][0] == np.array([0., 1., 2.])))
        self.assertTrue(all(ut['spike_times'][1] == np.array([3., 4., 5.])))

    def test_get_obs_intervals(self):
        ut = ICEphysUnits()
        ut.add_unit(obs_intervals=[[0., 1.]])
        ut.add_unit(obs_intervals=[[2., 3.], [4., 5.]])
        self.assertTrue(np.all(ut.get_unit_obs_intervals(0) == np.array([[0., 1.]])))
        self.assertTrue(np.all(ut.get_unit_obs_intervals(1) == np.array([[2., 3.], [4., 5.]])))

    def test_obs_intervals(self):
        ut = ICEphysUnits()
        ut.add_unit(obs_intervals=[[0., 1.]])
        ut.add_unit(obs_intervals=[[2., 3.], [4., 5.]])
        self.assertTrue(np.all(ut['obs_intervals'][0] == np.array([[0., 1.]])))
        self.assertTrue(np.all(ut['obs_intervals'][1] == np.array([[2., 3.], [4., 5.]])))

    def test_times_and_intervals(self):
        ut = ICEphysUnits()
        ut.add_unit(spike_times=[0., 1., 2.], obs_intervals=[[0., 2.]])
        ut.add_unit(spike_times=[3., 4., 5.], obs_intervals=[[2., 3.], [4., 5.]])
        self.assertTrue(all(ut['spike_times'][0] == np.array([0., 1., 2.])))
        self.assertTrue(all(ut['spike_times'][1] == np.array([3., 4., 5.])))
        self.assertTrue(np.all(ut['obs_intervals'][0] == np.array([[0., 2.]])))
        self.assertTrue(np.all(ut['obs_intervals'][1] == np.array([[2., 3.], [4., 5.]])))

    def test_electrode(self):
        ut = ICEphysUnits()
        device = Device(name='device_name')
        elec = IntracellularElectrode(name='test_iS',
                                      device=device,
                                      description='description',
                                      slice='slice',
                                      seal='seal',
                                      location='location',
                                      resistance='resistance',
                                      filtering='filtering',
                                      initial_access_resistance='initial_access_resistance')
        ut.add_unit(electrode=elec)
        self.assertIs(ut['electrode'][0], elec)


class TestICEphysUnitsIO(AcquisitionH5IOMixin, TestCase):
    """ Test adding Units into acquisition and accessing Units after read """

    def setUpContainer(self):
        """ Return the test Units to read/write """
        ut = ICEphysUnits(description='a simple table for testing ICEphysUnits')
        self.device = Device(name='device_name')
        self.elec = IntracellularElectrode(name='test_iS',
                                           device=self.device,
                                           description='description',
                                           slice='slice',
                                           seal='seal',
                                           location='location',
                                           resistance='resistance',
                                           filtering='filtering',
                                           initial_access_resistance='initial_access_resistance')
        ut.add_unit(spike_times=[0., 1., 2.], obs_intervals=[[0., 1.], [2., 3.]], electrode=self.elec)
        ut.add_column(name='foo', description='an int column', data=[1])
        ut.add_column(name='my_bool', description='a bool column', data=[False])
        ut.add_unit(spike_times=[3., 4., 5.], obs_intervals=[[2., 5.], [6., 7.]], electrode=self.elec, foo=30,
                    my_bool=True)
        return ut

    def addContainer(self, nwbfile):
        """ Add the test IntracellularElectrode, Device, and ICEphysUnits to the given NWBFile """
        nwbfile.add_device(self.device)
        nwbfile.add_ic_electrode(self.elec)
        nwbfile.add_acquisition(self.container)

    def test_get_spike_times(self):
        """ Test whether the Units spike times read from file are what was written """
        ut = self.roundtripContainer()
        received = ut.get_unit_spike_times(0)
        np.testing.assert_array_equal(received, [0., 1., 2.])
        received = ut.get_unit_spike_times(1)
        np.testing.assert_array_equal(received, [3., 4., 5.])
        np.testing.assert_array_equal(ut['spike_times'][:], [[0, 1, 2], [3, 4, 5]])

    def test_get_obs_intervals(self):
        """ Test whether the Units observation intervals read from file are what was written """
        ut = self.roundtripContainer()
        received = ut.get_unit_obs_intervals(0)
        np.testing.assert_array_equal(received, [[0., 1.], [2., 3.]])
        received = ut.get_unit_obs_intervals(1)
        np.testing.assert_array_equal(received, [[2., 5.], [6., 7.]])
        np.testing.assert_array_equal(ut['obs_intervals'][:], [[[0., 1.], [2., 3.]], [[2., 5.], [6., 7.]]])


class TestICEphysUnitsExample(TestCase):
    # from README.md
    from pynwb import NWBFile, NWBHDF5IO
    from datetime import datetime

    nwbfile = NWBFile(session_description='session_description',
                      identifier='identifier',
                      session_start_time=datetime.now().astimezone())

    # create a Device, IntracellularElectrode (refers to Device) in the NWB file
    device = nwbfile.create_device(name='device_name')
    electrode = nwbfile.create_ic_electrode(name='test_iS',
                                            device=device,
                                            description='description',
                                            slice='slice',
                                            seal='seal',
                                            location='location',
                                            resistance='resistance',
                                            filtering='filtering',
                                            initial_access_resistance='initial_access_resistance')

    # create a ICEphysUnits (refers to IntracellularElectrode)
    units = ICEphysUnits(description='Identified units from thresholded spiking activity')
    units.add_unit(spike_times=[0., 1., 2.], obs_intervals=[[0., 1.], [2., 3.]], electrode=electrode)

    # add the ICEphysUnits to the NWB file
    nwbfile.add_acquisition(units)

    # write to file
    save_path = 'test_out.nwb'
    with NWBHDF5IO(save_path, 'w') as io:
        io.write(nwbfile)

    # read from file
    with NWBHDF5IO(save_path, 'r') as io:
        read_nwbfile = io.read()
        print(read_nwbfile)
