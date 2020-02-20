# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec
# TODO: import the following spec classes as needed
from pynwb.spec import NWBDatasetSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""Table to hold detected spike times from intracellular ephys recordings""",
        name="""ndx-icephys-units""",
        version="""0.1.0""",
        author=list(map(str.strip, """Ryan Ly""".split(','))),
        contact=list(map(str.strip, """rly@lbl.gov""".split(',')))
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types
    ns_builder.include_type('DynamicTable', namespace='core')
    ns_builder.include_type('VectorData', namespace='core')
    ns_builder.include_type('VectorIndex', namespace='core')
    ns_builder.include_type('IntracellularElectrode', namespace='core')

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information

    spike_times_index = NWBDatasetSpec(
        name='spike_times_index',
        neurodata_type_inc='VectorIndex',
        doc=('Index into the spike_times dataset.'),
        quantity='?'
    )

    spike_times = NWBDatasetSpec(
        name='spike_times',
        neurodata_type_inc='VectorData',
        dtype='float64',
        doc=('Spike times for each unit.'),
        quantity='?',
        attributes=[
            NWBAttributeSpec(
                name='resolution',
                doc=('The smallest possible difference between two spike times. Usually 1 divided by the acquisition '
                     'sampling rate from which spike times were extracted, but could be larger if the acquisition '
                     'time series was downsampled or smaller if the acquisition time series was '
                     'smoothed/interpolated and it is possible for the spike time to be between samples.'),
                dtype='float64',
                required=False
            )
        ],
    )

    obs_intervals_index = NWBDatasetSpec(
        name='obs_intervals_index',
        neurodata_type_inc='VectorIndex',
        doc=('Index into the obs_intervals dataset.'),
        quantity='?'
    )

    obs_intervals = NWBDatasetSpec(
        name='obs_intervals',
        neurodata_type_inc='VectorData',
        dtype='float64',
        doc=('Observation intervals for each unit.'),
        quantity='?',
        dims=['num_intervals', 'start|end'],
        shape=[None, 2]
    )

    electrode = NWBDatasetSpec(
        name='electrode',
        neurodata_type_inc='VectorData',
        dtype=NWBRefSpec(target_type='IntracellularElectrode',
                         reftype='object'),
        doc=('Electrode that each unit came from.'),
        quantity='?',
    )

    waveform_mean = NWBDatasetSpec(
        name='waveform_mean',
        neurodata_type_inc='VectorData',
        dtype='float32',
        doc=('Spike waveform mean for each unit.'),
        quantity='?',
        dims=['num_units', 'num_samples'],
        shape=[None, None],
        attributes=[
            NWBAttributeSpec(
                name='sampling_rate',
                doc='Sampling rate, in hertz.',
                dtype='float32',
            ),
            NWBAttributeSpec(
                name='unit',
                doc="Unit of measurement. This value is fixed to 'volts'.",
                dtype='text',
                value='volts'
            ),
        ],
    )

    waveform_sd = NWBDatasetSpec(
        name='waveform_sd',
        neurodata_type_inc='VectorData',
        dtype='float32',
        doc=('Spike waveform standard deviation for each unit.'),
        quantity='?',
        dims=['num_units', 'num_samples'],
        shape=[None, None],
        attributes=[
            NWBAttributeSpec(
                name='sampling_rate',
                doc='Sampling rate, in hertz.',
                dtype='float32',
            ),
            NWBAttributeSpec(
                name='unit',
                doc="Unit of measurement. This value is fixed to 'volts'.",
                dtype='text',
                value='volts'
            ),
        ],
    )

    icephys_units = NWBGroupSpec(
        neurodata_type_def='ICEphysUnits',
        neurodata_type_inc='DynamicTable',
        doc=('A DynamicTable to hold detected spike times from intracellular ephys recordings.'),
        datasets=[
            spike_times_index,
            spike_times,
            obs_intervals_index,
            obs_intervals,
            electrode,
            waveform_mean,
            waveform_sd
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [icephys_units]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
