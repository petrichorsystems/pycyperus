''' setup.py
This file is a part of 'pycyperus'
This program is free software: you can redistribute it and/or modify
hit under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'pycyperus' is a python api for cyperus-server

Copyright 2024 murray foster '''


from setuptools import setup

setup(
    name='pycyperus',
    version='0.1.0',    
    description='a python api for cyperus-server',
    url='https://github.com/petrichorsystems/pycyperus',
    author='murray foster',
    author_email='mrafoster@gmail.com',
    license='BSD 2-clause',
    packages=['pycyperus'],
    install_requires=['python-osc>=1.9.0',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.13',
    ],
)
