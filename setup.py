from setuptools import setup

setup(name='traclus_impl',
      version='0.3',
      description='First pass implementation of traclus algorithm',
      url='http://github.com/apolcyn/traclus_impl.git',
      author='AP',
      author_email='alexpolcyn65@gmail.com',
      license='MIT',
      packages=['traclus_impl'],
      install_requires=[
          'polypaths_planar_override',
      ],
      zip_safe=False)
