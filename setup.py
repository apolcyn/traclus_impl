from setuptools import setup

LONG_DESCRIPTION = open('README.md', 'r').read()

setup(name='traclus_impl',
      version='0.9.8',
      url='http://github.com/apolcyn/traclus_impl.git',
      author='Alex Polcyn',
      author_email='alexpolcyn65@gmail.com',
      description='Implementation of Traclus for 2-D trajectories', 
      license='MIT',
      packages=['traclus_impl', 
      'traclus_impl.tests', 
      'traclus_impl.tests.clustering', 
      'traclus_impl.tests.coordination', 
      'traclus_impl.tests.partitioning', 
      'traclus_impl.integ_tests',
      'traclus_impl.integ_tests.representative_line_segments',
      'traclus_impl.integ_tests.post_processing_connection_finding',
      'traclus_impl.integ_tests.partitioning',
      'traclus_impl.integ_tests.parameter_estimation',
      'traclus_impl.integ_tests.deer_tests',
      'traclus_impl.integ_tests.coordination'],
      package_data={'traclus_impl.integ_tests': ['*.txt'], 
	      'traclus_impl.integ_tests.deer_tests': ['*.tra', '*.txt']},
      install_requires=[
	  'simanneal',
	  'click',
      ],
      zip_safe=False)
