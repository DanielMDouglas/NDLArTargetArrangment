# generate a geometry using the opencascade interface
# if called as a standalone script, save that geometry
# to a step file named 'cathodeTargetArray.step'

import numpy as np
from netgen.occ import *
import yaml

from targetGeometry import *

def generate_cathode_geo():
    # make a rough outline of the cathode shape
    CathodeShape = Box(Pnt(-cathode_width/2, -cathode_width/2, -cathode_thickness),
                       Pnt(cathode_width/2, cathode_width/2, 0))

    return CathodeShape

def load_cathode_geo(filename):
    # load the cathode shape from a step file
    return OCCGeometry(filename)

def generate_dot_targets(targetFile):
    # load the target configuration from file
    # read the 'dots' info and generate them

    with open(targetFile, 'r') as targetDesc:
        yamlDesc = yaml.load(targetDesc,
                             Loader = yaml.CLoader)
        dot_locations = yamlDesc['dots']
    
    dots = [Cylinder(Pnt(*(np.array(loc) + cathode_center)),
                     Z,
                     r = dot_radius,
                     h = dot_thickness)
            for loc in dot_locations]

    return dots

def generate_line_targets(targetFile):
    # load the target configuration from file
    # read the 'lines' info and generate them

    with open(targetFile, 'r') as targetDesc:
        yamlDesc = yaml.load(targetDesc,
                             Loader = yaml.CLoader)
        line_endpoints = yamlDesc['lines']

    lines = []
    for endpoints in line_endpoints:
        # the two points are the centers of the circles
        # at each end of the lines
        pointA, pointB = endpoints
        pointA = np.array(pointA) + cathode_center
        pointB = np.array(pointB) + cathode_center
        cylA = Cylinder(Pnt(*pointA),
                        Z,
                        r = line_radius,
                        h = line_thickness)
        cylB = Cylinder(Pnt(*pointB),
                        Z,
                        r = line_radius,
                        h = line_thickness)

        # join the two ends with a rectangle
        # so the "line" is a thick line with circular ends
        length = np.sqrt(np.sum(np.power(pointA - pointB, 2)))
        box = Box(Pnt(*(pointA + \
                        np.array([0, -line_radius, 0]))),
                  Pnt(*(pointA + \
                        np.array([length, line_radius, line_thickness]))))
        angle = np.arctan2((pointB[1] - pointA[1]), (pointB[0] - pointA[0]))
        print (np.degrees(angle))
        box = box.Rotate(Axis(Pnt(*pointA),
                              Z),
                         np.degrees(angle))

        lines.append(cylA + cylB + box)
        
    return lines

def main(args):
    # load the cathode geometry
    cathGeo = load_cathode_geo(args.cathodeFile)

    # load the target config
    dotsList = generate_dot_targets(args.targetFile)
    linesList = generate_line_targets(args.targetFile)

    # glue them together into one solid
    geo = Glue([cathGeo.shape] + dotsList + linesList)

    # write them as a step file
    geo.WriteStep(args.outfileName)
    
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description = 'use netgen to mesh a geometry (in step format) and export')
    parser.add_argument('-c', '--cathodeFile',
                        default = '',
                        help = 'input cathode brep')
    parser.add_argument('-t', '--targetFile',
                        default = '',
                        help = 'input target layout yaml')
    parser.add_argument('-o', '--outfileName',
                        default = 'cathodeTargetArray.step',
                        help = 'output step file name (default: cathodeTargetArray.step)')
    
    args = parser.parse_args()

    main(args)
