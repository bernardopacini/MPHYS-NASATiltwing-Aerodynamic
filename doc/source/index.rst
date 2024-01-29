NASA Tiltwing Vehicle - Aerodynamic Optimization
================================================

The NASA tiltwing concept vehicle is a research model developed for urban air mobility research.
The six passenger vehicle features a tilting wing that is vertical for takeoff and landing, but horizontal for climb and cruise.
The design has eight propellers, with six across the main wing and two on the tail.
The propellers are all used for both hover and cruise flight modes.
The tiltwing design in both flight modes is shown schematically below.

.. subfigure:: AB
   :layout-sm: A|B
   :gap: 8px
   :subcaptions: below
   :name: NASA tiltwing concept vehicle
   :class-grid: outline

   .. image:: ./images/TiltwingHover.png
      :alt: (a)

   .. image:: ./images/TiltwingCruise.png
      :alt: (b)

   Schematics of the NASA tiltwing concept vehicle in (a) hover and (b) cruise configurations.

This work uses the tiltwing design as a benchmark for understanding the effect of distributed propulsion design on wing design.
The vehicle's wing is simulated and optimized with no propellers through five propellers, spaced along the wing span.
The nominal flight condition is the one defined for cruise, which specifies a density of 0.9049 kg/m :math:`^3`, a freestream velocity of 79.74 m/s, a pressure of 69,692.1456 Pa, and a temperatre of 268.35K.
For more infomration about the tiltwing design, please checkout the `design report <https://ntrs.nasa.gov/api/citations/20210017971/downloads/NASA-TM-20210017971.pdf>`_.

This guide details the pre-processing, solving, and post-processing steps necessary to recreate the analyses and optimizations in our work.
Checkout the following sections to for details on how we generated the geometry, meshed the case, parameterized the wing, and ran the optimizations.

.. toctree::
   :caption: Pre-Processing
   :maxdepth: 2

   preProcessing/index
   preProcessing/geometryGeneration
   preProcessing/meshGeneration
   preProcessing/geometryParameterization

.. toctree::
   :caption: Solving
   :maxdepth: 2

   solving/index
   solving/propellerDefinition
   solving/optimizationRunscript

.. toctree::
   :caption: Post-Processing
   :maxdepth: 2

   postProcessing/index
   postProcessing/optimizationHistory
   postProcessing/aerodynamicResults
