import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spriteutil_final",
    version="1.0.4",
    author="Long Lam Duc",
    author_email="long.lam@f4.intek.edu.vn",
    description="A sprite detection package",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/intek-training-jsc/sprite-detection-longlamduc.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)