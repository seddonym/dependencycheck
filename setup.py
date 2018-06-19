from setuptools import setup, find_packages
setup(
    name="dependencycheck",
    version="0.0.1",
    packages=find_packages(),
    install_requires=(
        'networkx>=2.1,<3',
        'pydeps>=1.5.1,<2',
        'PyYAML>=3.12,<4',
    ),
    entry_points={
        'console_scripts': [
            'dependencycheck = dependencycheck.cmdline:main',
        ],
    },
)