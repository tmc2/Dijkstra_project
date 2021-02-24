# Dijkstra project
|Py-Versions| |Versions| |Build-Status| 
|LICENCE| 
This is a project for the Algorithms and Data Structures class lessioned at CIn-UFPE on 2020.2.

## Introduction
This project uses data from Brightkite (old location-based social networking service provider) provided by (http://snap.stanford.edu/data/loc-Brightkite.html) to find the closest path between mutual friends using their locations.

The idea is that travelers could plan their trip by tracing a route that uses friend's houses as stops. Lowering the overall cost of the travel and enhancing their safety.

The Djikstra algorithm was applied here to find the minimum path between two friends, suggesting other friends along the way and using the distance between their location as edges' weights.

## Installation
You can simply clone this repository and use as it is.
You will only need Python 3.5 (or above) installed.

## Usage
There are two Python scripts that you can run simply by calling it.
.. code:: python
    python <script_name>.py

If you want to run the pre-processing script, you will need to download the original data from http://snap.stanford.edu/data/loc-Brightkite.html and place it into Data folder.

The ``main.py`` requires only the pre-processed data that is already provided on the ``Data`` folder.
Run and follow de instructions printed on console to either check the least path for two friend users or to check the greatest minimum distance from one user to all friends.

## Authors
* [Thiago Chaves]

## License
Open source licensed under the MIT license (see _LICENSE_ file for details).
