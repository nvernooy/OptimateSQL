"""
setyp.py contains the set of modules required by this package
and sets up the enviroment for pyramid
"""

from setuptools import setup

requires = [
    'pyramid',
    'pyramid_chameleon',
]

setup(name='Optimate_Pyramid',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = Optimate_Pyramid:main
      """,
)
