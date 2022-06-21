from setuptools import setup

__author__ = 'Long LAM DUC'
__copyright__ = 'Copyright (C) 2019, Intek Institute'
__email__ = 'longlamduc@f4.intek.edu.vn'
__license__ = 'MIT'
__maintainer__ = 'Long Lam Duc'
__version__ = '1.0.0'
__name__ = "spriteutil"

setup(
    author=__author__,
    author_email=__email__,
    name= __name__,
    copyright = __copyright__,
    license = __license__,
    maintainer = __maintainer__,
    version = __version__,
    install_requires=[
        "numpy==1.22.0",
        "Pillow==6.2.0",
    ]
)