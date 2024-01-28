Overview
========

Aerodynamic shape optimization requires a set of tools for repeated aerodynamic analyses of many geometry iterations.
Once the pre-processing stage of generating a geometry, mesh, and parameterization is complete, the optimization beings.
The aerodynamic shape optimization workflow is shown below, as an eXtended Design Structure Matrix diagram.
Each iteration begins with the optimizer providing a set of design variables to the geometry parameterization.
These geoemtry changes displace the FFD, which subsequently deform the aerodynamic surface mesh of the wing.
This step is carried out by DVGeo, within the pyGeo package.
Once the geometry update is complete, the surrounding volume mesh is deformed to match the computational grid to the new geometry using IDwarp.
This computation grid is then solved using an aerodynamic solver, in this case DAFoam, to compute the performance of the wing.
From the converged solution, the functional values needed for the optimization, in this case lift and drag, are computed and passed back to the optimizer.
Along with the baseline values, the tools provide model derivatives to enable gradient-based optimization.
This optimzation cycle is repeated until the design converges to an optimal design.

.. figure:: ../images/aerodynamicXDSM.pdf

   eXtended Design Structure Matrix of aerodynamic shape optimization including the optimizer block, geometry parameterization, mesh warping, aerodynamic solver, and post-processor functionals.

The optimization investigated in this work is shown in the table below.
For each propeller configuration, the wing drag is minimized with respect to a variety of physical and geometric constraints.
The design freedom includes 8 twist design variables and 160 shape design variables.
The twist each FFD section about the Y-axis while the shape variables deform the wing surface locally in the Z-direction.

| *minimize*
|    :math:`C_D`
| *with respect to*
|    8 twist variables
|    160 shape variables
| *subject to*
|    :math:`C_L = 0.67`
|    :math:`V_0 \le V \leq 3V_0`
|    :math:`0.5t_0 \le t \le 3t_0`
|    :math:`R_{LE} \ge R_{LE,0}`
|    :math:`\Delta z_\text{LETE, upper} = -\Delta z_{LETE, lower}`

The optimization is subject to a lift constraint of :math:`C_L = 0.67` to satisfy the lift required in cruise flight.
The optimization must also satisfy a set of geometric constraints.
Volume and thickness constraints are used to represent considerations required by structural and packaging constraints that are not accounded for in aerodynamic optimization.
Similarly, a leading edge radius constraint is used to ensure the optimizer does not make a wing with a sharp leading edge that would be impractical at all other flight conditions.
Finally, the leading edge and trailing edge shape variables are tied together to ensure that they can not cause shape induced twist, ensuring orthogonality in the design space.

This optimization is carried out using the MACH framework embedded with OpenMDAO and MPhys.
The following sections detail the code components to run the case.
