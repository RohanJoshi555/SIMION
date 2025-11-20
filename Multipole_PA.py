import numpy as np
from SIMION.PA import *

def hollowCylinder(pa, inner_diameter, outer_diameter, length, x_center, y_center, z_center, Potential):
    '''
    Creates a cylindrical electrode.
    The units of length for radius, length, x_center, etc are in grid units.
    Potential - Potential of electrode in Volts.
    '''
    for z in range(pa.nz()):
        for y in range(pa.ny()):
            for x in range(pa.nx()):
                if z_center - (length/2) <= z and z <= z_center + (length/2):
                    dx = x-x_center; dy = y-y_center
                    axial_distance = np.sqrt(dx**2 + dy**2)
                    if inner_diameter/2 <= axial_distance and axial_distance <= outer_diameter/2:
                        pa.point(x,y,z,1,Potential)

## Order of multipole/number of rods 
n = 22
## Geometric parameters of multipole in mm
# 1. Rods and the inscribing circle
rod_dia_mm = 2.0
rod_length_mm = 40.0
icircle_dia_mm = rod_dia_mm * (n/2-1)
print("Inscribing circle's diameter =",icircle_dia_mm,"mm")

## Setting scale
# Grid units per mm
gu_per_mm = 5
# Distance b/w 2 successive grid points in mm/grid unit
scale = 1/gu_per_mm
print('Scale = ',scale,'mm/gu')

## Converting the user entered dimensions from mm to grid units
rod_dia_gu = rod_dia_mm * gu_per_mm
rod_length_gu = rod_length_mm * gu_per_mm
icircle_dia_gu = icircle_dia_mm * gu_per_mm

## Creating a Potential Array(PA)
pa2 = PA(nx = floor(icircle_dia_gu + rod_dia_gu + 20), 
         ny = floor(icircle_dia_gu + rod_dia_gu + 20), 
         nz = floor(rod_length_gu + 50))
print('Number of array points: nx = ',pa2.nx(),' ny = ',pa2.ny(),' nz = ',pa2.nz())

## Create multipole: n electrode rods distributed uniformly(touching) on an inscribing circle
rod_dia_gu = rod_dia_mm * gu_per_mm
rod_length_gu = rod_length_mm * gu_per_mm
icircle_dia_gu = icircle_dia_mm * gu_per_mm
R = (icircle_dia_gu + rod_dia_gu)/2
z_center = pa2.nz()/2
icircle_xcenter = pa2.nx()/2
icircle_ycenter = pa2.ny()/2
thetavals = np.linspace(0, 2*np.pi, n, endpoint = False)
rod_count = 0
for theta in thetavals:
    rod_count += 1
    Volt = rod_count
    x_center = icircle_xcenter + R*np.cos(theta)
    y_center = icircle_ycenter + R*np.sin(theta)
    hollowCylinder(pa2, 0, rod_dia_gu, rod_length_gu, x_center, y_center, z_center, Volt)
    print('Rod',rod_count,'Created.')

pa2.save("D:\\MSc_Project\\SIMION 8.0-20250825T144631Z-1-001\\SIMION 8.0\\mystuff\\2d_22_pole_ion_trap2\\22_pole.pa#")
print("Potential array created.")