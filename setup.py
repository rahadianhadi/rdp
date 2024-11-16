from setuptools import setup, find_packages

setup(
    name='rdp',
    version='0.1.0',
    description='Utility tools for Python and Django framework.',
    author='Rahadian Hadi',
    author_email='rahadianhadi@gmail.com',
    url='https://github.com/rahadianhadi/rdp',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.0',
    ],
    entry_points={
        'console_scripts': [
            'rdp=rdp.cli:main',
        ],
    },
)
