#!/usr/bin/python
"""
    Rfm2Rfk
    Copyright (C) 2025 Suolin Zhang, Bournemouth University

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Author: Suolin Zhang
    e-mail: s5705957@bournemouth.ac.uk
    ------------------------------
    Copy Renderman shading network from Maya to Katana
    ------------------------------
"""


__version__ = "0.0.1"


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import importlib
from Rfm2Rfk import utils
importlib.reload(utils)

from Rfm2Rfk import m2k
importlib.reload(m2k)

copy = m2k.copy
del m2k


