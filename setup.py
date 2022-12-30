import os
import re
import setuptools

# Get version based on Javabridge setup functions

def pep440_compliant(ver):
    if ver is None:
        return ver
    m = re.match(r"^(?P<version>(\d[\d\.]*))$", ver)
    if m:
        return ver
    m = re.match(r"^(?P<version>([v]\d[\d\.]*))-(?P<count>\d+)-(?P<sha>.*)$", ver)
    if m:
        res = m.group('version') + '.post' + m.group('count') + '+' + m.group('sha')
        return res
    return ver

def get_version():
    """Get version from git or file system.

    If this is a git repository, try to get the version number by
    running ``git describe``, then store it in
    bioformats/_version.py. Otherwise, try to load the version number
    from that file. If both methods fail, quietly return None.

    """
    git_version = None
    if os.path.exists(os.path.join(os.path.dirname(__file__), '.git')):
        import subprocess
        try:
            # get all tags, including non-annotated ones
            git_version = subprocess.Popen(
                ['git', 'describe', '--tags'],
                stdout=subprocess.PIPE).communicate()[0].strip().decode('utf-8')
        except:
            print("could not find")
            pass

    version_file = os.path.join(os.path.dirname(__file__), 'bioformats',
                                '_version.py')
    if os.path.exists(version_file):
        with open(version_file) as f:
            cached_version_line = f.read().strip()
        try:
            # From http://stackoverflow.com/a/3619714/17498
            cached_version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                                       cached_version_line, re.M).group(1)
        except:
            raise RuntimeError("Unable to find version in %s" % version_file)
    else:
        cached_version = None

    if git_version and git_version != cached_version:
        try:
            with open(version_file, 'w') as f:
                print('__version__ = "%s"' % git_version, file=f)
        except FileNotFoundError as e:
            print("Unable to create version file, skipping")

    return pep440_compliant(git_version or cached_version)

setuptools.setup(
    author="Lee Kamentsky",
    author_email="leek@broadinstitute.org",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Java",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion"
    ],
    description="Read and write life sciences file formats",
    extras_require={
        "test": [
            "pytest>=3.3.2,<4"
        ],
        "aws": [
            "boto3>=1.14.23",
        ],
    },
    install_requires=[
        "future>=0.18.2",
        "javabridge"
    ],
    license="GPL License",
    long_description="""Python-bioformats is a Python wrapper for Bio-Formats, a standalone Java library for reading
    and writing life sciences image file formats. Bio-Formats is capable of parsing both pixels and metadata for a
    large number of formats, as well as writing to several formats. Python-bioformats uses the python-javabridge to
    start a Java virtual machine from Python and interact with it. Python-bioformats was developed for and is used by
    the cell image analysis software CellProfiler (cellprofiler.org).  While we are gratified that others
    outside the CellProfiler team find it useful, we maintain python-bioformats essentially for the CellProfiler project 
    and **cannot currently guarantee support for other users.** Please consider visiting our forum at forum.image.sc for 
    additional support help.""",
    name="python-bioformats",
    package_data={
        "bioformats": [
            "jars/*.jar"
        ]
    },
    packages=[
        "bioformats"
    ],
    url="http://github.com/CellProfiler/python-bioformats/",
    version=get_version(),
)
