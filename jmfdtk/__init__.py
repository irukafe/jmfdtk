import os

from .__version__ import __version__

JMFD_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'jmfd',
    'J-MFD_2018r1_mod.dic'
)

from jmfdtk.utils import _display
from jmfdtk.counter import jmfcounter
from jmfdtk.clustering import clustering
from jmfdtk.khcodegen import generate_khcode
from jmfdtk.jmfdloader import load_jmfd
