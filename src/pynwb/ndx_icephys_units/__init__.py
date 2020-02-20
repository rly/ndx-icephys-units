import os
from pynwb import load_namespaces

# Set path of the namespace.yaml file to the expected install location
ndx_icephys_units_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-icephys-units.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_icephys_units_specpath):
    ndx_icephys_units_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-icephys-units.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_icephys_units_specpath)

from .icephys_units import ICEphysUnits  # noqa: E402, F401
