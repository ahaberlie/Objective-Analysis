# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 03:19:21 2016

@author: Alex
"""

import numpy as np

from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter


def get_points_within_r(center_point, target_points, r, return_idx=False):
    '''Get all target_points within a specified radius 
    of a center point.  All data must be in same coord-
    inate system, or you will get unpredictable results.
    
    Parameters
    ----------
    center_points: (X, Y) ndarray
        location from which to grab surrounding points within r
    target_points: (X, Y) ndarray
        points from which to return if they are within r of center_points
    r: integer
        search radius around center_points to grab target_points
    return_idx: bool
        If true, function will return indices of winning points
        If false (default), function will return list of winning points
    
    Returns
    -------
    (X, Y) ndarray
        A list of points within r distance of, and in the same 
        order as, center_points    
    '''
    
    tree = cKDTree(target_points)
    indices = tree.query_ball_point(center_point, r)
    return tree.data[indices].T

    
def get_point_count_within_r(center_points, target_points, r):
    '''Get count of target points within a specified radius 
    from center points.  All data must be in same coord-
    inate system, or you will get unpredictable results.
    
    Parameters
    ----------
    center_points: (X, Y) ndarray
        locations from which to grab surrounding points within r
    target_points: (X, Y) ndarray
        points from which to return if they are within r of center_points
    r: integer
        search radius around center_points to grab target_points
    
    Returns
    -------
        A list of point counts within r distance of, and in the same 
        order as, center_points    
    '''
    
    tree = cKDTree(target_points)
    indices = tree.query_ball_point(center_points, r)
    return np.array([len(x) for x in indices])
    

def smoothed_freq_map(x_points, y_points, bbox, x_steps, y_steps, gaussian):
    '''Create smoothed spatial frequency map of points per user
    defined grid cell within a specified extent.  All values are
    assumed to be in the same coordinate system.
    
    Parameters
    ----------
    x_points: array-like
        x_coordinates used to calculate counts per grid cell
    y_points: array-like
        y_coordinates used to calculate counts per grid cell
    bbox: dictionary of boundary coordinates
        spatial bounding box of histogram
    steps: (X_size, Y_size) ndarray
        size of the grid cells
    gaussian: floating point
        size of smoothing window
    
    Returns
    -------
        A smoothed frequency grid    
    '''
    
#    west = bbox['southwest'][0]
#    north = bbox['northeast'][1]
#    east = bbox['northeast'][0]
#    south = bbox['southwest'][1]
    
    grid, _, _ = np.histogram2d(y_points, x_points, bins=(y_steps, x_steps))
    grid = np.flipud(grid)
    return gaussian_filter(grid, sigma=gaussian)


def generate_grid(x_dim, y_dim, bbox):
    
    x_steps, y_steps = get_xy_steps(bbox, x_dim, y_dim)
    grid_x = np.linspace(bbox['northeast'][0], bbox['southwest'][0], x_steps)
    grid_y = np.linspace(bbox['northeast'][1], bbox['southwest'][1], y_steps)
    
    gx, gy = np.meshgrid(grid_x, grid_y)
    
    return gx, gy
    

def generate_grid_coords(gx, gy):
    
    return np.vstack([gx.ravel(), gy.ravel()]).T

def get_xy_range(bbox):
    
    x_range = bbox['southwest'][0] - bbox['northeast'][0] 
    y_range = bbox['northeast'][1] - bbox['southwest'][1]
    
    return x_range, y_range
    
def get_xy_steps(bbox, x_dim, y_dim):
    
    x_range, y_range = get_xy_range(bbox)
    
    x_steps = int(round(x_range / x_dim, 0) + 1)
    y_steps = int(round(y_range / y_dim, 0) + 1)
    
    return x_steps, y_steps
    
def get_boundary_coords(x, y):
    
    west = np.max(x)
    east = np.min(x)
    north = np.max(y)
    south = np.min(y)
    
    return {'southwest': (west, south), 'northeast': (east, north)}
    
    