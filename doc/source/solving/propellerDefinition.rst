Propeller Definition
====================

The tiltwing vehicle is designed with three propellers on each wing, all of equal size.
The propellers are equally spaced along the wing, with the propeller disks tangent to each other.
The purpose of this study is to understand the effect of changing the number of propellers along the wing.
Configurations with no propellers through five propellers are optimized using actuator zone representations of the propellers.
These configurations are shown in the following figure, detailing the size and location of each propeller.
For a given configuration, the propellers are assumed to be identical in design and operating condition.

.. subfigure:: ABC|DEF
   :layout-sm: A|B|C|D|E|F
   :gap: 8px
   :subcaptions: below
   :name: Distributed propulsion configurations
   :class-grid: outline

   .. image:: ../images/Setup0.png
      :alt: (a)

   .. image:: ../images/Setup1.png
      :alt: (b)

   .. image:: ../images/Setup2.png
      :alt: (c)
      
   .. image:: ../images/Setup3.png
      :alt: (d)

   .. image:: ../images/Setup4.png
      :alt: (e)

   .. image:: ../images/Setup5.png
      :alt: (f)

   Schematics of the distributed propulsion configurations with varying number of propellers. (a) No propellers, (b) 1 propeller, (c) 2 propellers, (d) 3 propellers, (e) 4 propellers, and (f) 5 propellers.

The propellers' location, size, and thrust for each configuration are parameterized using a simple helper function that is called at the start of the optimization.
These values are used in DAFoam to define the actuator zones embedded in the flowfield.
This file is found at ``/wingOnly/setupRotors.py``.

The function that defines the propellers is called ``fvSourceDict()`` and takes in the number of propellers, returning the required DAFoam actuator zone dictionary.
The total thrust of the propellers is held constant across all configurations and the inboard edge of the inboard propeller disk is assumed to be the furthest inboard allowable for the propeller disks.
Using these limitations, actuator zones are interpolated along the length of the wing span, sharing the same dimensions and thrust requirements.
The cases with two through five propellers occupy the complete wing span.
However, the single propeller is limited by installation effects, to avoid the actuator zone intersecting the wing.

.. literalinclude:: ../../../wingOnly/setupRotors.py
    :start-after: # rst fvSourceDict
    :end-before: # rst setupRotors debug

To checkout the values associated with each configuration, the script can be called in isolation and it will print out the associated DAFoam dictionary.
To do this, navigate to the ``wingOnly/`` directory and run the Python script:

.. prompt:: bash

    python setupRotors.py
