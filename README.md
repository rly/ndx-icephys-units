# ndx-icephys-units Extension for NWB

## Installation

```bash
pip install ndx-icephys-units
```

## Usage

```python
from pynwb import NWBFile, NWBHDF5IO
from datetime import datetime
from ndx_icephys_units import ICEphysUnits

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
```


This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
