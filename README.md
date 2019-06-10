# triton (WIP)

## Introduction

This extends Amphitrite with a client-server architecture graphical interface based on modern web technologies (Electron, Dash, Plotly, Javascript) with a back-end running on Python 3.

The original Amphitrite code-base was ported from Python 2.x to Python 3.x using automated tools as well as manual formatting of the original code (a number of functions have to be re-written in order to sucesfully run in the new environment)

## Structure

IPC Client Server Architecture with a Renderer/Main process and a Flask server to server the front-end.

## How to run

A virtual environment can be created in order to run the program but it's main structure is quite simple:

Run the `python3 ichor/amphitrite.py` to create a server process that will provide a local server on a predefined port (5000 by default but that can be changed). When this is sucesfull the Electron part of the application can be started by running `electron .` which will install the respective `node_modules` and run the front-end.
