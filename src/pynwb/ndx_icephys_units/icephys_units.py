import numpy as np
from bisect import bisect_left, bisect_right

from hdmf.common import DynamicTable
from hdmf.utils import docval, getargs, call_docval_func, get_docval

from pynwb import register_class
from pynwb.icephys import IntracellularElectrode


# adapted from pynwb.misc.Units but to store intracellular units
@register_class('ICEphysUnits', 'ndx-icephys-units')
class ICEphysUnits(DynamicTable):
    """A DynamicTable to hold detected spike times from intracellular ephys recordings."""

    __columns__ = (
        {'name': 'spike_times', 'description': 'Spike times for each unit', 'index': True},
        {'name': 'obs_intervals', 'description': 'Observation intervals for each unit', 'index': True},
        {'name': 'electrode', 'description': 'Electrode that each spike unit came from.'},
        {'name': 'waveform_mean', 'description': 'Spike waveform mean for each unit'},
        {'name': 'waveform_sd', 'description': 'Spike waveform standard deviation for each unit'}
    )

    @docval({'name': 'name', 'type': str, 'doc': 'Name of this ICEphysUnits table', 'default': 'ICEphysUnits'},
            *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'),
            {'name': 'description', 'type': str, 'doc': 'Description of what is in this table', 'default': None})
    def __init__(self, **kwargs):
        if kwargs.get('description', None) is None:
            kwargs['description'] = "Data on spiking units"
        call_docval_func(super().__init__, kwargs)
        if 'spike_times' not in self.colnames:
            self.__has_spike_times = False

    @docval({'name': 'spike_times', 'type': 'array_data', 'doc': 'Spike times for each unit',
             'default': None, 'shape': (None,)},
            {'name': 'obs_intervals', 'type': 'array_data',
             'doc': ('Observation intervals (valid times) for each unit. All spike_times for a given unit '
                     'should fall within these intervals. [[start1, end1], [start2, end2], ...]'),
             'default': None, 'shape': (None, 2)},
            {'name': 'electrode', 'type': IntracellularElectrode,
             'doc': 'Electrode that each unit came from', 'default': None},
            {'name': 'waveform_mean', 'type': 'array_data',
             'doc': 'Spike waveform mean for each unit. Shape is (time,)', 'default': None, 'shape': (None,)},
            {'name': 'waveform_sd', 'type': 'array_data',
             'doc': 'Spike waveform standard deviation for each unit. Shape is (time,)', 'default': None,
             'shape': (None,)},
            {'name': 'id', 'type': int, 'default': None, 'doc': 'ID for each unit'},
            allow_extra=True)
    def add_unit(self, **kwargs):
        """Add a unit to this table."""
        super().add_row(**kwargs)

    @docval({'name': 'index', 'type': (int, list, tuple, np.ndarray),
             'doc': 'the index of the unit in unit_ids to retrieve spike times for'},
            {'name': 'in_interval', 'type': (tuple, list), 'doc': 'only return values within this interval',
             'default': None, 'shape': (2,)})
    def get_unit_spike_times(self, **kwargs):
        """Get spike times for a unit within the given time interval."""
        index, in_interval = getargs('index', 'in_interval', kwargs)
        if type(index) in (list, tuple):
            return [self.get_unit_spike_times(i, in_interval=in_interval) for i in index]
        if in_interval is None:
            return np.asarray(self['spike_times'][index])
        else:
            st = self['spike_times']
            unit_start = 0 if index == 0 else st.data[index - 1]
            unit_stop = st.data[index]
            start_time, stop_time = in_interval

            ind_start = bisect_left(st.target, start_time, unit_start, unit_stop)
            ind_stop = bisect_right(st.target, stop_time, ind_start, unit_stop)

            return np.asarray(st.target[ind_start:ind_stop])

    @docval({'name': 'index', 'type': int,
             'doc': 'the index of the unit in unit_ids to retrieve observation intervals for'})
    def get_unit_obs_intervals(self, **kwargs):
        """Get the observation intervals for a given unit"""
        index = getargs('index', kwargs)
        return np.asarray(self['obs_intervals'][index])
