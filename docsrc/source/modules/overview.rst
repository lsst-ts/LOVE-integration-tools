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
It is built as a Python module that uses salobj and websockets to produce messages between SAL and the LOVE-manager. “Messages” can be understood without distinction as events or telemetries .
For more details check the `LOVE-producer docs <https://lsst-ts.github.io/LOVE-producer/html/index.html>`_.

LOVE-CSC
--------
The `LOVE-CSC <https://github.com/lsst-ts/LOVE-producer/tree/develop/producer/love_csc>`_ is defined in the :code:`LOVE-producer` repository, it is a :code:`CSC` that provides an HTTP API to accept requests with observing logs messages and dispatches the observing logs event using :code:`salobj`.
For more details check the `LOVE-producer docs <https://lsst-ts.github.io/LOVE-producer/html/index.html>`_.

LOVE-commander
--------------
The `LOVE-commander <https://github.com/lsst-ts/LOVE-commander>`_ is a backend application that acts as middleware between the LOVE-manager and SAL.
It is built as a Python module that provides and HTTP API to accept command requests and run them using :code:`salobj`, and provide some SAL information, such as metadata, topics names, among others.
For more details check the `LOVE-commander docs <https://lsst-ts.github.io/LOVE-commander/html/index.html>`_.

LOVE-simulator
--------------
The `LOVE-simulator <https://github.com/lsst-ts/LOVE-simulator>`_ repository contains different Python modules used to simulate the software components of a real LSST environment interacting with SAL.
It is meant to be used for development and testing purposes.

Database
--------------
The :code:`Database` is used by the :code:`LOVE-manager` to store users, their permissions and access tokens, the UI Framework views, among others. It is currently a :code:`PostgreSQL` instance.

Channels Layer
--------------
The :code:`Channels Layer` is used by the :code:`LOVE-manager` as a message queue for the websockets messages. It is currently a :code:`Redis` instance.


LOVE Architecture
=================
.. image:: ../assets/LOVE_arch.svg

As shown in the figure above, the :code:`LOVE-frontend` is executed in the client browser (as it is a web application) while the rest of the components are executed in the LSST Servers.
The :code:`LOVE-frontend` communicates with the rest of the system through the :code:`LOVE-manager`. The :code:`LOVE-frontend` sends users credentials to login and then established a websocket connection with the :code:`LOVE-manager` to receive data from it.

The :code:`LOVE-manager` gets the data from the :code:`LOVE-Producer` and :code:`LOVE-Commander` through a websocket and HTTP. The :code:`LOVE-Producer` and :code:`LOVE-Commander` interacts with the rest of the system through the Software Abstraction Layer (:code:`SAL`).
The rest of the system consists on Commandable SAL Components (:code:`CSCs`) which interact with each other through :code:`SAL`.

Additionally, observing logs are sent from the :code:`LOVE-frontend` to the :code:`LOVE-manager` and from there to the :code:`LOVE-CSC` thorugh websockets. The :code:`LOVE-CSC` dispatches an event with the observing log message using :code:`salobj`.
The event then arrives to the :code:`LOVE-frontend` through the same path as any other event, though the :code:`LOVE-producer` and :code:`LOVE-manager`,

CSCs communication consists in 4 types:

- Telemetries: values that represent a software or hardware measurement in the real world
- Events: that are triggered upon some defined conditions, for example, when a critical condition is reached, or when a process has finished.
- Commands: instructions for another CSC to execute an action.
- Command Acknowledgements: acknowledgements of sucessful command executions, sent for the CSC that sent the command.

We also developed the :code:`LOVE-simulator`, for development and testing purposes, which acts as a "fake" :code:`CSC` that sends data and commands to :code:`SAL`, replicating the behavior of some defined :code:`CSCs`.


LOVE Deployment
=================
.. image:: ../assets/LOVE_deployment.svg

The figure above shows how the LOVE components are currently being deployed. They are all orquestrated with :code:`docker-compose` and are present in the :code:`Docker` network.
Additionally, the components that interact with the :code:`SAL/DDS` are also part of the DDS Network. This way they can interact with other :code:`CSC` outside the :code:`Docker` network.

It is worth to mention that different instances of the :code:`LOVE-producer` are deployed, each of them takins care of different message, namely: telemetries, events, heartbeats, ScriptQueue state.
For more deatils about this please refere to the `LOVE-producer docs <https://lsst-ts.github.io/LOVE-producer/html/index.html>`_.

The user interacts with the LOVE system through a :code:`Nginx` instance, that acts as load balancer and URL router. Routing requests to the :code:`LOVE-frontend` and :code:`LOVE-manager` accordingly.