Optimization History
====================

The optimization histories for all six optimizations are shown in the figure below.
Using SNOPT, the optimality and feasibility for each optimization are recorded.
While the specified tolerance of the optimization was not achieved for any case and they instead reached the maximum number of iterations, they did achieve the desired two order of magniture decrease in optimality.
Conversely, the feasibility did achieve tight tolerances across all of the optimizations.
The coefficient of drag shows decreases in the first 50 iterations, but the remaining iterations show little improvement.
The coefficient of lift instead shows deviation from the desired value for the first 100 iterations, but then stabilizes for all cases and remains at the constraint value for the remainder of the optimizations.

.. figure:: ../images/optHist.pdf

   Optimization convergence history showing the optimality, feasibility, coefficient of drag, and coefficient of lift for each optimization.

The improvement in coefficient of drag for all configurations are shown below.
Each case shows approximately 6% improvement from the baseline design, with the single propeller case provig to be the best design.
This result is consistent for both the baseline and optimized results, showing that a single propeller helps the design the most, with decreasing improvement as the number of propellers is increased.
Aerodynamic shape optization does not affect this trend.

.. figure:: ../images/optCD.pdf

   Optimization results for each propeller configuration showing the baseline and optimized coefficients of drag and the resulting percentage improvement.

Another study investigated in this work is to understand the importance of optimizing considering propeller effects.
The wing optimized without the propeller was trimmed for each propeller configuration, to understand if optimization with propeller effects provides significantly improved results.
The trimmed coefficients of drag for each case, included below, show there is nearly no difference in performance between the wings opitmized with propellers and the trimmed, optimized no propeller wing.

.. figure:: ../images/optCDProp0.pdf

   Percentage difference in coefficient of drag between optimized wings considering propeller influence and the no propeller wing, trimmed for each configuration.
