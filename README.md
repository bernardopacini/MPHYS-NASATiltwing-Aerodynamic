NASA Tiltwing Vehicle - Aerodynamic Optimization
================================================

[![Documentation Status](https://readthedocs.org/projects/mphys-nasatiltwing-aerodynamic/badge/?version=latest)](https://mphys-nasatiltwing-aerodynamic.readthedocs.io/en/latest/?badge=latest)

This repository holds the runscripts and files used for aerodynamic optimization of the NASA tiltwing concept vehicle's wing.
The scripts contained in this repository can be used to recreate a study into distributed propulsion on an urban air mobility concept vehicle.
This work was originally presented at the AIAA SciTech forum:

```Bernardo Pacini, Malhar Prajapati, Karthikeyan Duraisamy, Joaquim R. Martins and Ping He. "Understanding Distributed Propulsion on the NASA Tiltwing Concept Vehicle with Aerodynamic Shape Optimization," AIAA 2023-0143. AIAA SCITECH 2023 Forum. January 2023.```

Beware that the exact results presented in the paper may differ from results generated with newer versions of the tools used in the study.
Checkout the paper, documentation, and runscripts for the exact details of the project as well as the necessary files to recreate the work.

Documentation
-------------

Documentation for the mesh and geometry parameterization, as well as the runscripts, is included in the `/doc` directory.
The documentation is written in `reStructuredText` and automatically uploaded to `ReadTheDocs`.
To generate the documentation locally, ensure you have a working Python3 installation with `sphinx` and `sphinx-prompt` installed.
Navigate to the `doc/` directory and execute:

```
make html
open build/html/index.html
```

Otherwise, checkout the [online documentation](https://mphys-nasatiltwing-aerodynamic.readthedocs.io/en/latest/).

Case Files
-----------

To avoid bloading the repository, many files used in the optimizations are not tracked with Git.
These include files such as the free-form deformation parameterization, the geometry objects, and the meshes.
Some of these files are generated while pre-processing the case, while others can be downloaded directly from our storage drive.

To download the files, install the Python package `gdown`, navigate to the `inputData/` directory, and run the `getData.sh` script.
This will download and unpack the required files needed for the cases.

Dependencies
------------

These optimizations require a variety of dependencies that include fundamental tools such as GCC / GNU, MPI, and PETSc, as well as the MACH optimization framework.
For information on how to install DAFoam and the required dependencies, checkout the [online installation guide](https://dafoam.github.io/mydoc_installation_source.html).

DAFoam also ships as a Docker image.
To avoid installing DAFoam and the associated environment from scratch, checkout the [pre-packaged image](https://dafoam.github.io/mydoc_get_started_download_docker.html).

Contributors
------------

* Bernardo Pacini
* Malhar Prajapati
* Karthik Duraisamy
* Joaquim R R A Martins
* Ping He

Additional Notes
----------------

* The optimizations run for this study were run on the Great Lakes Cluster within the Advanced Research Computing center at the University of Michigan. We recommend about 128 cores and 200GB of RAM to run the cases.
