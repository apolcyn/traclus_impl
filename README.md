# traclus_impl

### Purpose
This is a Python implementation of the Traclus algorithm. 
It works for 2-D trajectories. 

This was written for a senior project that involved clustering GPS trajectories of pedestrians on a school campus; I found that this worked well for that.
Other implementations of Traclus exist, but I didn't see one in Python and thought this could be useful for my project and possibly elsewhere.
This traclus implementation should functionally work, but it has room to be sped up. Note that if you are able
to use the rtree python package, then clustering can use an r-tree for neighbor queries instead of quadratic lists.

### Install
The easiest way to install is with pip install traclus_impl.

### Installing with rtree
If you're able to install rtree, then clustering can use an
Rtree instead of plain list searching. "rtree" is listed as a dependency in the optional-requirements.txt file, 
but it will not get included by default.
See https://pypi.python.org/pypi/Rtree/ for installation.

### Usage
To run the Traclus algorithm, run traclus_impl.main.py, passing it the name of an input file and output file.
The input file contains a json object with parameters to traclus and the raw trajectories.
See "traclus_impl.integ_tests.raw_campus_trajectories.txt" for an example input file.
The output file will contain a json list of representative trajectories.
Optionally, provide names of files to dump the output from the partitioning and clustering stages too.

Example: navigate to directory where traclus_impl.main.py is and run "python main.py -i ./raw_traj_input -o ./traclus_output

Note that the actual entry point function of the real computation is "run_traclus" in traclus_impl.coordination.py.
The "run_traclus" function takes Traclus arguments and a list of trajectories. The list of trajectories input to "run_traclus"
is a list of traclus_impl.geometry.Point objects, and it returns a list of representative line segments as this same type of object.

main.py only parses arguments to traclus, calls run_traclus, and writes them to a file. 
It is mostly just an example of a way to use the "run_traclus" function.

The best example of complete usage is the test in "traclus_impl.integ_tests.campus_trajectories_processing_test.py".

### Parameters
The parameters to this mostly match up to what's in the paper, but this allows you to be a little more specific.

* epsilon: Same as description in the paper. 
* min_neighbors: Minimum number of neighboring line segments for a line segment to be considered a "core line sigment" (as described in the paper).
See "Definition 5" in the paper.
* min_num_trajectories_in_cluster: Minimum number of participating trajectories in a cluster after clustering is done in order for the cluster to be kept.
See "Definition 10" in the paper.
* min_vertical_lines: Same as the "MinLns" parameter described in the representative trajectory generation algorithm of the paper.
* min_prev_dist: The smoothing parameter described in the representative trajectory generation algorithm of the paper.

### Intermediate output hooks
The "run_traclus" function in traclus_impl.coordination.py optionally takes hooks for the output of
the partitioning stage and clustering stage. The hook functions for these in main.py and the 
"traclus_impl.integ_tests.campus_trajectories_processing_test.py" tests show some example usage.

Note that the clusters passed to the clusters output hook include all clusters formed, before filtering out the ones that didn't have enough unique trajectories.
In my project, I used this to find the "entropy" with Formula 10 in the paper.

### parameter estimation
There is code for simulated annealing and computing "entropy" based on formula 10 in the paper. This uses the simmanneal python package to do this.
The code for it is in parameter_estimation.py. An example is in the traclus_impl.integ_tests.parameter_estimation.simulated_annealing_tests.py test.
In my project, I ran simulated annealing with the clusters_output hook computing the entropy on each step, and had decent results.

### Running the tests.
Tests exist under the traclus_impl.tests and traclus_impl.integ_tests.
To run all of the tests from the commandline (assuming the package is installed), navigate to the package's root and run: python -m unittest discover -p "\*_test*.py"
If using bash, run the ./tests.sh to run tests without it needing to be installed (but it's dependencies do).
Note that a message will appear on stderr telling whether or not rtree is being used. If it's not installed, 
the rtree tests are skipped.

### Notes on the code
* A lot of this was just me messing around with unit testing and manual mocks, which explains a lot of the passing of functions as 
parameters that you might find when looking at the code.

* The distance function math is in distance_functions.py and geometry.py

* in coordination.py, "run_traclus" first removes points in the trajectories that are too close, and then calls "the_whole_enchilada", which runs traclus.
Zero-length line segments need to be removed first just to let everything else run smooth.

### Notes on Performance
* Currently, the main bottleneck seems to be the quadratic clustering, and future work includes improving this.
For some larger trajectory sets such as the elk file under integ_tests/deer_tests, this implementation will take a very long time.
* traclus_impl.integ_tests.deer_tests.run_traclus.py is mostly used for profiling this traclus implementation on the trajectories in that folder.
