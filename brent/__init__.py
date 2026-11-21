# TODO: docstrings
# TODO: type hinting
# TODO: standardise datetime/timedelta type (probably NumPy)
# TODO: fix bug where THALASSA breaks following the use of Matplotlib

# Standard imports
import os
import sys
import shutil

# Load paths
from . import paths

# Register MinGW runtime DLL directory on Windows
if os.name == "nt":
    compiler = shutil.which("gfortran")
    if compiler is not None:
        _mingw_dll_directory = os.add_dll_directory(
            os.path.dirname(compiler)
        )

# Orekit imports
import orekit
from orekit.pyhelpers import setup_orekit_curdir

# Initialise Orekit. Suppress macOS OpenJDK stack-guard warnings emitted at VM startup.
orekit.initVM()
setup_orekit_curdir(paths.DATA_OREKIT_DIR)

# Add PyTHALASSA to path
sys.path.append(paths.THALASSA_LIB_DIR)

# Load constants
from .constants import Constants

# Internal imports
from . import bias
from . import covariance
from . import filter
from . import frames
from . import io
from . import propagators
from . import util
from . import skyfield
