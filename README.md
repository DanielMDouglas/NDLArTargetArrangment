# NDLArTargets
This package provides some utilities for building CAD models of DUNE ND-LAr cathodes with attached photocathodes.  These can be used as inputs for CAD workflows downstream.  The advantage of this program is to provide a programmatic way to generate target arrays, as well as producing yaml descriptions of the target arrangments that can be used in analysis workflows

## Usage

The package provides two main pieces of code, which can be called as scripts.  The first step is to generate a target description yaml using `target_yaml_generator.py`:

```
usage: target_yaml_generator.py [-h] [-o OUTFILE]

generate a yaml file containing target configuration

options:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        output yaml file name (default: targetConfiguration.yaml)
```

Calling it with default arguments will produce a yaml file containing the locations of the dot-type and line-type targets as they are described within the script.  If you want to alter, this arrangement, please edit this script, particularly the `generate_dot_locations` and `generate_line_locations` functions!

The next step is to combine this yaml file with an existing cathode CAD model using netgen's OCC interface.  This is done by calling `make_cathod.py`:

```
usage: make_cathode.py [-h] [-c CATHODEFILE] [-t TARGETFILE] [-o OUTFILENAME]

use netgen to mesh a geometry (in step format) and export

options:
  -h, --help            show this help message and exit
  -c CATHODEFILE, --cathodeFile CATHODEFILE
                        input cathode brep (default: cathodeGeometries/cathode.step)
  -t TARGETFILE, --targetFile TARGETFILE
                        input target layout yaml (default: targetConfiguration.yaml)
  -o OUTFILENAME, --outfileName OUTFILENAME
                        output step file name (default: cathodeTargetArray.step)
```

With default arguments, after generating the target arrangement yaml, this will produce a new step file containing the specified target shapes superimposed onto the input cathode shape.  This model can be further processed in your favorite CAD workflow to prepare it for 3D printing or some other process.