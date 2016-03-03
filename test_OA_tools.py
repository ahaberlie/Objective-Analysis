# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 04:27:27 2016

@author: Alex
"""

import numpy as np
from numpy.testing import assert_array_equal

from OA_tools import get_boundary_coords
from OA_tools import get_xy_steps
from OA_tools import get_xy_range


def test_get_boundary_coords():
    'Test 1d nearest neighbor functionality.'
    x = np.arange(1000.)
    y = np.arange(1000.)
    truth = {'southwest': (np.max(x), np.min(y)), 'northeast': (np.min(x), np.max(y))}

    assert_array_equal(truth, get_boundary_coords(x, y))

def test_get_xy_steps():
    
    x = np.arange(1000.)
    y = np.arange(1000.)
    
    bbox = get_boundary_coords(x, y)
    
    x_dim = 100
    y_dim = 100
    
    truth = np.array((10, 10))
    
    assert_array_equal(truth, get_xy_steps(bbox, x_dim, y_dim))
    
    
    
    