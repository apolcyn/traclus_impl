# traclus_impl

### Purpose
This is a Python implementation of the Traclus algorithm. 
It works for 2-D trajectories. 
Note that this was written as a piece of a senior project. 
This traclus implementation should functionally work, but it is currently slow on larger sets of trajectories.

### Install
The easiest way to install is with pip install traclus_impl.

### Usage
To run the Traclus algorithm, run traclus_impl.main.py, passing it the name of an input file and output file.
The input file contains a json object with parameters to traclus and the raw trajectories.
See "traclus_impl.integ_tests.raw_campus_trajectories.txt" for an example input file.
The output file will contain a json list of representative trajectories.
Optionally, provide names of files to dump the output from the partitioning and clustering stages to.

Example: navigate to directory where traclus_impl.main.py is and run "python main.py -i ./raw_traj_input -o ./traclus_output

Note that the actual entry point function of the real computation is "run_traclus" in traclus_impl.coordination.py.
The "run_traclus" function takes Traclus arguments and a list of trajectories. The list of trajectories input to "run_traclus"
is a list of traclus_impl.geometry.Point objects, and it returns a list of representative line segments as this same type of object.

main.py only parses arguments to traclus, calls run_traclus, and writes them to a file. 
It is mostly just an example of a way to use the "run_traclus" function.

The best example of complete usage is the test in "traclus_impl.integ_tests.campus_trajectories_processing_test.py".

### Intermediate output hooks ###
The "run_traclus" function in traclus_impl.coordination.py optionally takes hooks for the output of
the partitioning stage and clustering stage. The hook functions for these in main.py and the 
"traclus_impl.integ_tests.campus_trajectories_processing_test.py" tests show some example usage.

### Running the tests.
Tests exist under the traclus_impl.tests and traclus_impl.integ_tests.
To run all of the tests from the commandline, navigate to the package's root and run: python -m unittest discover -p "*_test*.py"

### Notes on Performance ###
* Currently, the main bottleneck seems to be the quadratic clustering, and future work includes improving this.
For some larger trajectory sets such as the elk file under integ_tests/deer_tests, this implementation will take a very long time.
* traclus_impl.integ_tests.deer_tests.run_traclus.py is mostly used for profiling this traclus implementation on the trajectories in that folder.

