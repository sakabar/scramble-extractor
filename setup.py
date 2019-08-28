from setuptools import setup

setup(
    name="info.saxcy.scramble_extractor",
    version="0.0.1",
    install_requires=[
	'docopt',
    ],
    extras_require={
        'test': [
            'pytest',
            ],
    },
    entry_points={}
)
