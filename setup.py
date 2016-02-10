from setuptools import setup

setup(name='traclus_impl',
      version='0.6',
      description='First pass implementation of traclus algorithm',
      url='http://github.com/apolcyn/traclus_impl.git',
      author='AP',
      author_email='alexpolcyn65@gmail.com',
      license='MIT',
      packages=['traclus_impl', 'traclus_impl.partitioning', \
       'traclus_impl.traclus_dbscan'], 
      install_requires=[
          'polypaths_planar_override',
      ],
      zip_safe=False)
