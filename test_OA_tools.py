# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 04:27:27 2016

@author: Alex
"""

from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import OA_tools

from mpl_toolkits import basemap
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

plt.rcParams['figure.figsize'] = (12, 10)

torData = pd.read_csv('https://raw.githubusercontent.com/ahaberlie/hovmoller/master/torn_reports_minimal.csv',delimiter=',',header=0)
print(torData)

torDat = torData[((torData.LON<-60) & (torData.LON>-130)) & ((torData.LAT>20) & (torData.LAT<60))]

lats = np.array(torDat['LAT'])
lons = np.array(torDat['LON'])

m = basemap.Basemap(
    width=4800000, height=3100000, projection='aea', resolution='l',
    lat_1=28.5, lat_2=44.5, lat_0=38.5, lon_0=-97.,area_thresh=5000)
    
x_proj, y_proj = m(lons, lats)
tor_points_proj = list(zip(x_proj, y_proj))

b_box = OA_tools.get_boundary_coords(x_proj, y_proj)

#m.plot(x_proj,y_proj,'k.',markersize=1)
#m.drawcoastlines()
#m.drawstates()
#m.drawcountries()
#plt.title("All touchdowns 1950-2013")

okc_pt = m(-97.5350, 35.4822)
radius = 500000

x_near, y_near = OA_tools.get_points_within_r(okc_pt, tor_points_proj, radius)

m.plot(x_near, y_near,'k.',markersize=1)

xmin = np.min(x_near)
xmax = np.max(x_near)
ymin = np.min(y_near)
ymax = np.max(y_near)
plt.axis([xmin, xmax, ymin, ymax]) #zoom in to radius

m.drawcoastlines()
m.drawstates()
m.drawcountries()
plt.title("All touchdowns 1950-2013 within " + str(round(radius / 1000,0)) + "km of OKC.")

search_radius = 100000
search_area = np.pi * search_radius**2

x_res = y_res = 10000

b_box = OA_tools.get_boundary_coords(x_near, y_near)
gx, gy = OA_tools.generate_grid(x_res, y_res, b_box)
grid_points = OA_tools.generate_grid_coords(gx, gy)


x_steps, y_steps = OA_tools.get_xy_steps(b_box, 40000, 40000)

print(x_steps, y_steps)
grid = OA_tools.smoothed_freq_map(x_proj, y_proj, b_box, x_steps, y_steps, 6)
#counts = OA_tools.get_point_count_within_r(grid_points, list(zip(x_near, y_near)), search_radius)
#
#counts = counts / search_area * (1000**2)
#
#x_steps, y_steps = OA_tools.get_xy_steps(b_box, x_res, y_res)
#vals = np.array(counts).reshape(y_steps, x_steps)
#
#levels = MaxNLocator(nbins=6).tick_values(np.min(vals), np.max(vals))
#
#cmap = plt.get_cmap('coolwarm')
#norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
#
#plt.pcolormesh(gx, gy, vals, cmap=cmap, norm=norm)
#m.drawstates()
#
##m.plot(x_proj,y_proj,'k.',markersize=1)
#
##plt.axis([xmin, xmax, ymin, ymax]) #zoom in to radius
#m.drawcoastlines()
#m.drawstates()
#m.drawcountries()
#plt.title("Tornado touchdown Density per km" + r"$^2$" + ", 1950-2013")
#cbar = plt.colorbar(shrink=.4,pad=.02,orientation='horizontal')
#cbar.set_label(str(x_res/1000) + "x" + str(y_res/1000) + "km" + r"$^2$" + " grids" + str(search_radius/1000) + " search radius")