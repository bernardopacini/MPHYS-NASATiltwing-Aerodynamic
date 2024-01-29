Optimization Runscript
======================

The analysis, derivative checks, and optimization for all configurations is carried out with a single Python script.
This script defines the optimization problem, imports the baseline mesh and geometry parameterization, and coordinates what the desired task is.
All of the underlying tools are unified through Python and hidden from the user, making the optimization easier to configure at the top level.
The runscript is included at ``/wingOnly/runScriptAerodynamic.py``.

The runscript begins with importing the necessary packages.
These packages include generic Python packages for interfacing with files and performing computation.
In addition to generic imports, the MACH, OpenMDAO, and MPhys packages must be imported.
For this case, these include the baseline MPhys `Multipoint` class and aerodynamic scenario, the DAFoam MPhys wrapper, and the pyGeo MPhys wrapper.
In addition to the required packages, the previously defined `setupRotors` script is imported so that it can be called at runtime to define propeller configurations.

.. literalinclude:: ../../../wingOnly/runScriptAerodynamic.py
    :start-after: # rst imports
    :end-before: # rst parser

An argument parser is used in the script to allow the user to quick switch between tasks.
This is done using the Python argument parser.

.. literalinclude:: ../../../wingOnly/runScriptAerodynamic.py
    :start-after: # rst parser
    :end-before: # rst flight condition

The next part of the script that must be defined is the flight condition.
This tiltwing optimization is carried out in the cruise flight configuration, defined by:

.. literalinclude:: ../../../wingOnly/runScriptAerodynamic.py
    :start-after: # rst flight condition
    :end-before: # rst daOptions

These cruise flight parameters are used when setting up the optimization and underlying DAFoam / OpenFOAM case.
This part of the script also defines the target coefficient of lift, number of propellers, and FFD file.

Once the fundamental components are imported and the flight condition is defined, the DAFoam options are initialized.
This includes a variety of options that detail the design surfaces, solver and boundary parameters, functionals of interest, and the adjoint solver configuration.

These cases optimize the wing geometry and solve the surrounding flow with `DARhoSimpleFoam`.
The primal boundary conditions are set through this runscript in accordance with the prescribed flight condition.
The primal variable bounds are defined to improve the robustness of the solver and the actuator zones, defined in the ``fvSourceDict`` are defined using the associated propeller definition script.
This optimization focuses on the wing's lift and drag, so we define two functionals of interest: ``CD`` and ``CL``.
With these instructions, DAFoam will compute these values and the corresponding derivatives for the optimizer.
The defined adjoint options prescribe the convergence tolerance of the adjoint solver, as well as the jacobian ordering and preconditioner settings.
Finally, the DAFoam options define the associated design variables and mesh quality thresholds.
These parameters are used to initailize and govern the DAFoam primal and adjoint solvers through the optimization.

.. literalinclude:: ../../../wingOnly/runScriptAerodynamic.py
    :start-after: # rst daOptions
    :end-before: # rst class

The optimizations fundamentally depend on MPhys, a standardized framework for high-fidelity optimization built on OpenMDAO.
For MPhys, the top-level group of the optimization is an instance of the ``Multipoint`` Python class:

.. literalinclude:: ../../../wingOnly/runScriptAerodynamic.py
    :start-after: # rst class
    :end-before: # rst setup

This class contains a ``setup`` and a ``configure`` method.
The setup method is used to define the underflying groups and components needed for the optimization.
The first step of the setup is to initialize the DAFoam solver and required mesh parameters used for mesh warping.
Once the DAFoam object is initialized, we setup a group for the independent variables (``dvs``), a group to hold the mesh (``mesh``), a group that handles the geometry parameterization (``geometry``), and the MPhys scenario.
A scenario is a pre-build MPhys group that will handle connecting optimization components.
In this case we use an aerodynamic scenario titled ``cruise``, and provide it the DAFoam object.
To conclude the setup method, we connect the intial aerodynamic surface mesh to the geometry parameterization and the geometry parameterization to the cruise scenario.
At the start of the optimization, this setup will be run to define all of the defined components.

.. literalinclude:: ../../../wingOnly/runScriptAerodynamic.py
    :start-after: # rst setup
    :end-before: # rst configure

Following the setup phase, the configure method is called to continue setting up the optimization.
At this stage, the components needed for the optimization are defined, but they are not complete.
We begin by adding the functionals defined in the DAFoam options to the solver and add the aerodynamic surface points to the geometry component, with the name ``aero``.
We also embed a triangulated surface representation of the mesh as the constraint surface, needed for geometric constraints imposed by pyGeo.

We can then define design variables.
We start by setting up a reference axis in the FFD grid about which the FFD sections are rotated.
In this case, the axis extends in the Y-direction along the wing span and is located at the quarter chord line of the FFD grid.
We then define the twist variable function, provided to pyGeo and the DVGeo parameterization to impost the twist.
This is done by rotating the FFD coefficients at each section about the Y-axis, in accordance with the values assigned by the optimizer.
This function, along with baseline values, is provided to DVGeo.
Additionally, shape variables are assigned to deform the FFD in the Z-diretion, again through DVGeo.

With the design variables defined, we define the geometric constraints.
We begin by defining a set of leading edge and trailing edge lists.
These define lines that track the leading and trailing edges that are used for a few different constraints on thickness, volume, and leading edge radius.
The volume and thickness constraints define an ``nSpan`` by ``nChord`` set of "toothpick" constraints that form a grid between and long the leading and trailing edge lists.
The radius constraint is also defined using the leading edge list to compute the radius of the baseline leading edge.
An additional geometry constraint is imposed directly on the FFD grid to ensure that the shape variables do not impart shape induced twist, which would lead to duplicate twisting freedom.

With the constraints defined, baseline design variable outputs for twist and shape are initialized and connected to the geometry component.
At this point, the twist and shape variables are tagged as design variables and the physical and geometric constraints are tagged as constraints.
Finally, the coefficient of drag is defined as the objective.

.. literalinclude:: ../../../wingOnly/runScriptAerodynamic.py
    :start-after: # rst configure
    :end-before: # rst problem setup

With the OpenMDAO component setup and configured, the optimizer and problem settings are defined.
These include initializing the problem class and defining pyOptSparse as the optimization driver.
In this case, we use SNOPT and it's associated options as the optimizer, but both the driver and optimizer, and corresponding options, can be chaned as desired.
We initialize a recorder to retain the history of the optimization, and finally setup the complete case using reverse-mode derivatives.
We also generate an N2 diagram of the case with allows use to visualize the flow of data between all of the groups and components.


.. literalinclude:: ../../../wingOnly/runScriptAerodynamic.py
    :start-after: # rst problem setup
    :end-before: # rst tasks

.. raw:: html

    <a href="../images/n2.html">testurl</a>

At this point, the case is setup and ready for analysis, derivative check, or optimization.
The user has the ability to specify which task to run, according to the following pre-defined options.
The ``run_driver`` option runs the optimization, the ``run_model`` option performs a single model analysis, and the ``check_totals`` option computes the total derivatives of the optimization and compares them with finite-difference approximations.

.. literalinclude:: ../../../wingOnly/runScriptAerodynamic.py
    :start-after: # rst tasks

To run the case, use the following command and adjust it accordingly for the desired number of processors and task:

.. prompt:: bash

    mpirun -np <nProcs> runScriptAerodynamic.py --task=<task>

.. note::

    We ran these optimizations with 128 cores and several hundred gigabytes of RAM.
    While the analysis alone can be run on a reasonably capable computer, we recommend only running the derivative check and optimization on a powerful cluster.
