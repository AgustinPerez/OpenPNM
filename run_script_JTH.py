  # -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 00:00:01 2013
╛
@author: jhinebaugh
"""

import OpenPNM
from time import clock
import scipy as sp
clock()
stats_pores = {'name' : 'weibull_min',
                                     'shape' : 1.5,
                                       'loc' : .6,
                                     'scale' : 2.5}
stats_throats = {'name' : 'weibull_min',
                                     'shape' : 1.5,
                                       'loc' : .6,
                                     'scale' : 2.5}
print 'Creating 1,000 pore cubic network'
cubic = OpenPNM.Geometry.Cubic().generate(domain_size=[5,5,5],lattice_spacing=[1.0])
print 'Finished at time =',sp.round_(clock(),2),'seconds'
print ''
print 'Creating 100 pore Delauny network'
delaunay = OpenPNM.Geometry.Delaunay().generate(domain_size=[10,10,10],num_pores=100)
print 'Finished at time =',sp.round_(clock(),2),'seconds'
print ''
print 'Creating #### pore imported network'
matfile = OpenPNM.Geometry.MatFile().generate(filename='large_network')
print matfile
print 'Finished at time =',sp.round_(clock(),2),'seconds'
print ''
print "Adding 'air' and 'water' for each network type"
air_cubic = OpenPNM.Fluids.Air().create(fluid_name='air_cubic')
water_cubic = OpenPNM.Fluids.Water().create(fluid_name='water_cubic')
air_delaunay = OpenPNM.Fluids.Air().create(fluid_name='air_delaunay')
water_delaunay = OpenPNM.Fluids.Water().create(fluid_name='water_delaunay')
air_matfile = OpenPNM.Fluids.Air().create(fluid_name='air_matfile')
water_matfile = OpenPNM.Fluids.Water().create(fluid_name='water_matfile')
print ''
print "pairing fluids"
air_cubic.set_pair(water_cubic)
air_delaunay.set_pair(water_delaunay)
air_matfile.set_pair(water_matfile)
print ''
print 'Creating inlets and outlets'
inlets_cubic = cubic.pore_properties['numbering'][cubic.pore_properties['type']==1]
outlets_cubic = cubic.pore_properties['numbering'][cubic.pore_properties['type']==6]
inlets_delaunay = delaunay.pore_properties['numbering'][delaunay.pore_properties['type']==1]
outlets_delaunay = delaunay.pore_properties['numbering'][delaunay.pore_properties['type']==6]
inlets_matfile = matfile.pore_properties['numbering'][matfile.pore_properties['type']==1]
outlets_matfile = matfile.pore_properties['numbering'][matfile.pore_properties['type']==6]
print ''
print 'Running Invasion Percolation algorithm for cubic'
OpenPNM.Algorithms.InvasionPercolation().run(cubic,invading_fluid=water_cubic,inlets=inlets_cubic,outlets=outlets_cubic)
print ''
print 'Running Invasion Percolation algorithm for delaunay'
OpenPNM.Algorithms.InvasionPercolation().run(delaunay,invading_fluid=water_delaunay,inlets=inlets_delaunay,outlets=outlets_delaunay)
print ''
print 'Running Invasion Percolation algorithm for matfile'
OpenPNM.Algorithms.InvasionPercolation().run(matfile,invading_fluid=water_matfile,inlets=inlets_matfile,outlets=outlets_matfile)
print ''
print 'Running Ordinary Percolation algorithm for cubic'
OpenPNM.Algorithms.OrdinaryPercolation().run(network=cubic,invading_fluid=water_cubic,defending_fluid=air_cubic,inv_sites=inlets_cubic,npts=50,AL=True)
print ''
print 'Running Ordinary Percolation algorithm for delaunay'
OpenPNM.Algorithms.OrdinaryPercolation().run(network=cubic,invading_fluid=water_cubic,defending_fluid=air_cubic,inv_sites=inlets_cubic,npts=50,AL=True)
print ''
print 'Running Ordinary Percolation algorithm for matfile'
OpenPNM.Algorithms.OrdinaryPercolation().run(network=cubic,invading_fluid=water_cubic,defending_fluid=air_cubic,inv_sites=inlets_cubic,npts=50,AL=True)
print ''
print 'NEED MORE ALGORITHMS AND PHYSICS IN THIS TESTER. PLEASE ADD'
print ''
print 'writing VTK files'
OpenPNM.Visualization.VTK().write(cubic,water_cubic,'cubic.vtp')
OpenPNM.Visualization.VTK().write(delaunay,water_delaunay,'delaunay.vtp')
OpenPNM.Visualization.VTK().write(matfile,water_matfile,'matfile.vtp')

