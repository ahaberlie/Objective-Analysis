# Objective-Analysis

A Semi-unorganized collection of OA functions.  Some day I will make things cleaner.

Requirements thus far:

Python >= 3.4.3
Scipy >= 0.16
Numpy >= 1.10.1

Optional:

Pandas >= 0.17.1
Matplotlib >= 1.5.0
Basemap >= 1.0.8

Wrote some of the functions to remove annoyance from using KDTrees.

In particular, there was not a good way to get counts from a search radius query
on many points at the same time.  For example, assigning grids a value requires
many iterations with a nested loop, but is much faster if you send KDTree the
whole thing.

This is done using:

get_point_count_within_r(center_points, target_points, r)

In the notebook example I provide, the center_points are the grid cell 
projected coordinates, and the target_points are tornado touchdown locations.

similarly, to test a single point and return all points within radius r:

get_points_within_r(center_point, target_points, r, return_idx=False)

I will add an ability to get a list of a list of coordinates for each point.
My head kind of hurt thinking of how I'd try writing that docstring so I felt 
that was a good time to stop.