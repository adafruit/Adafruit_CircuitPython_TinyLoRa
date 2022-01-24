Introduction
============

.. image:: https://readthedocs.org/projects/circuitpython-tinylora/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/tinylora/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_TinyLoRa/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_TinyLoRa/actions/
    :alt: Build Status

**WARNING: This library is not compatible with The Things Network v3 stack. Since TTN has fully migrated to v3, this library is not longer able to communicate with TTN.**


LoRaWAN/The Things Network V2, for CircuitPython.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading `the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-tinylora/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-tinylora

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-tinylora

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-tinylora

Usage Example
=============

Usage is described in the `learn guide for this library <https://learn.adafruit.com/using-lorawan-and-the-things-network-with-circuitpython>`_.



Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/tinylora/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_TinyLoRa/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

License
=======
This library was written by ClemensRiederer. We've converted it to work with Adafruit CircuitPython and made
changes so it works with the Raspberry Pi and Adafruit Feather M0/M4. We've added examples for using this library
to transmit data and sensor data to The Things Network.

This open source code is licensed under the LGPL license (see LICENSE for details).
