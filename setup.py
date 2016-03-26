from setuptools import setup

LONG_DESCRIPTION = """First pass implementation of traclus algorithm.
This works with 2D trajectories. 
See the github for the unit tests and integ tests.

Note that this is being written as a piece of a senior project.
The implementation should functionally work, but the distance
functions need to be sped up and the code should be refactored
for readability."""


setup(name='traclus_impl',
      version='0.8.4',
      description=LONG_DESCRIPTION,
      url='http://github.com/apolcyn/traclus_impl.git',
      author='AP',
      author_email='alexpolcyn65@gmail.com',
      license='MIT',
      packages=['traclus_impl', \
      'traclus_impl.partitioning', \
      'traclus_impl.traclus_dbscan', \
      'traclus_impl.tests', \
      'traclus_impl.tests.clustering', \
      'traclus_impl.tests.coordination', \
      'traclus_impl.tests.partitioning'], 
      install_requires=[
	  'simanneal',
      ],
      zip_safe=False)
