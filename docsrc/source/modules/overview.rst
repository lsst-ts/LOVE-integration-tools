=====================
LOVE Project Overview
=====================

The LSST Operation and Visualization Environment (L.O.V.E.) project consists in the development of graphical user interfaces (GUI) for the monitoring and operation of the LSST.
The GUIs are built using web technologies in order to enable users access from different locations and different host systems.

This section provides a general overview of the LOVE project, how it is structured, how its software components interact, etc.
For usage instructions please refer to the :ref:`LOVE-integration-tools instructions` section.

LOVE Software repositories
==========================
The LOVE project is integrated by the following software components, each with its own repository

LOVE-frontend
-------------
The `LOVE-frontend <https://github.com/lsst-ts/LOVE-frontend>`_ is the web application that provides the LOVE GUIs.
It is built using `ReactJS <https://reactjs.org/>`_ to generate the static content (html, css and javascript files) of the LOVE web application.
For more details check the `LOVE-frontend docs <https://lsst-ts.github.io/LOVE-frontend/html/index.html>`_.

LOVE-manager
------------
The `LOVE-manager <https://github.com/lsst-ts/LOVE-manager>`_ is a backend application that acts as middleware for the LOVE-frontend.
It is built using `Django Channels <https://channels.readthedocs.io/en/latest/>`_ with `Redis <https://redis.io/>`_ as a `Channel Layer <https://channels.readthedocs.io/en/latest/topics/channel_layers.html>`_
For more details check the `LOVE-manager docs <https://lsst-ts.github.io/LOVE-manager/html/index.html>`_.

LOVE-producer
-------------
The `LOVE-producer <https://github.com/lsst-ts/LOVE-producer>`_ is a backend application that acts as middleware between the LOVE-manager and SAL.
It is built as a Python module that uses salobj and websockets to produce messages between SAL and the LOVE-manager. “Messages” can be understood without distinction as events, telemetries or commands parameters and their acknowledgements.
It is built using ReactJS to generate the static content (html, css and javascript files) of the LOVE web application.
For more details check the `LOVE-producer docs <https://lsst-ts.github.io/LOVE-producer/html/index.html>`_.

LOVE-simulator
--------------
The `LOVE-simulator <https://github.com/lsst-ts/LOVE-simulator>`_ repository contains different Python modules used to simulate the software components of a real LSST environment interacting with SAL.
It is meant to be used for development and testing purposes.


LOVE Components interaction
===========================
.. image:: ../assets/LOVE_overview.svg

As shown in the figure above, the LOVE-frontend is executed in the client browser (as it is a web application) while the rest of the components are executed in the LSST Servers.
The LOVE-frontend communicates with the rest fo the system through the LOVE-manager. The LOVE-frontend sends users credentials to login and then established a websocket connection with the LOVE-manager to receive data from it.

The LOVE-manager gets the data from the LOVE-Producer through a websocket connection. The LOVE-Producer interacts with the rest of the system through the Software Abstraction Layer (SAL).
The rest of the system consists on Commandable SAL Components (CSCs) which interact with each other through SAL.

CSCs communication consists in 4 types:

- Telemetries: values that represent a software or hardware measurement in the real world
- Events: that are triggered upon some defined conditions, for example, when a critical condition is reached, or when a process has finished.
- Commands: instructions for another CSC to execute an action.
- Command Acknowledgements: acknowledgements of sucessful command executions, sent for the CSC that sent the command.


We also developed the LOVE-simulator, for development and testing purposes, which acts as a "fake" CSC that sends data and commands to SAL, replicating the behavior of some defined CSCs.
