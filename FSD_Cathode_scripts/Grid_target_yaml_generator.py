#!/usr/bin/env python

import numpy as np
import yaml

def generate_dot_locations():

    # make a set of dot targets along the outer edge
    # with a relatively fine spacing
    nTargetsFine = 20
    xedgemm = 465  #474.29 in reality 
    yedgemm = 1475 #1484.29 in reality
    # this assumes that the cathode is at a constant
    # z coordinate (spans x-y)
    z = 0
    
    lin_target_den = 1/15   #one target per 20 mm 
    xTargetsFine = int(lin_target_den*2*xedgemm)
    yTargetsFine = int(lin_target_den*2*yedgemm)
    # make a set of targets along the outer edges
    bottom_row = [[float(xi), -yedgemm, z]
                  for xi in np.linspace(-xedgemm,
                                        xedgemm,
                                        xTargetsFine)]
    left_row = [[-xedgemm, float(yi), z]
                for yi in np.linspace(-yedgemm,
                                      yedgemm,
                                      yTargetsFine)[1:]]
    right_row = [[xedgemm, float(yi), z]
                 for yi in np.linspace(-yedgemm,
                                       yedgemm,
                                       yTargetsFine)[1:]]

    top_row = [[float(xi), yedgemm, z]
               for xi in np.linspace(-xedgemm,
                                     xedgemm,
                                     xTargetsFine)[1:-1]
               if abs(xi) > 40]
    
    #Generate grid of dots
    
    middle_rows = []

    num_rows = 40   #these are flipped of what they should be
    num_dots = 10
    edge_buffer = 50
    mid_xedgemm = xedgemm - edge_buffer
    mid_yedgemm = yedgemm - edge_buffer
    rows_x = np.linspace(-mid_xedgemm, mid_xedgemm ,num_dots)
    for x in rows_x:
        middle_rows += [[x, float(yi), z]
                        for yi in np.linspace(-mid_yedgemm,
                                              mid_yedgemm,
                                              num_rows)]
    '''                                        
    #Remove every other dot
    c = 0
    num_d = len(middle_rows)
    for i in range(0,num_d):    
        if c == 0:
            middle_rows.pop(num_d-1-i)
            c=1
        else :
            c=0'''
    
          
                                             
    # make a set of coarser targets towards the center
    # specified by hand
    """    coarse_dots = [[-60, 60, z],
                   [-100, 25, z],
                   [-100, -25, z],
                   [-60, -60, z],
                   [60, 60, z],
                   [100, 25, z],
                   [100, -25, z],
                   [60, -60, z],
                   [25, 25, z],
                   [25, -25, z],
                   [-25, 25, z],
                   [-25, -25, z],
                   [-25, -100, z],
                   [25, -100, z],
                   ]"""

    # combine all of the dot-type targets in a list
    dot_locations = sum([bottom_row,
                         left_row,
                         right_row,
                         top_row,
                         middle_rows,
                         ],
                        start = [])
    
    return dot_locations

def generate_line_locations():

    # make some line-like targets
    # these are defined by two points
    # the center of each circle that
    # terminates the lines
    
    z = 0

    top_left = [[-100, 75, z],
                [-75, 100, z]]
    top_right = [[100, 75, z],
                 [75, 100, z]]
    bottom_left = [[-75, -100, z],
                   [-100, -75, z]]
    bottom_right = [[75, -100, z],
                    [100, -75, z]]

    middle_top = [[-20, 60, z],
                  [20, 60, z]]
    middle_bottom = [[-20, -60, z],
                     [20, -60, z]]

    middle_left = [[-60, 20, z],
                   [-60, -20, z]]
    middle_right = [[60, 20, z],
                    [60, -20, z]]

    # add them all into one list
    line_locations = [top_left,
                      top_right,
                      bottom_left,
                      bottom_right,
                      middle_top,
                      middle_bottom,
                      middle_left,
                      middle_right,
                      ]
    
    return line_locations
    
def main(args):
    # generate the coordinates for each set of targets
    dots = generate_dot_locations()
    #lines = generate_line_locations()

    # put them into a dictionary for writing
    #targets = {'dots': dots,
               #'lines': lines}
    targets = {'dots': dots}

    # write them into a yaml
    with open(args.outfile, 'w') as outfile:
        outfile.write(yaml.dump(targets, Dumper = yaml.CDumper))
    
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description = 'generate a yaml file containing target configuration')
    parser.add_argument('-o', '--outfile',
                        default = 'targetConfiguration.yaml',
                        help = 'output yaml file name (default: targetConfiguration.yaml)')
    
    args = parser.parse_args()

    main(args)
