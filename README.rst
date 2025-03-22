===============================================
Material Dashboard with Bokeh embedded in Flask
===============================================

|Contributors| |License|

.. |Contributors| image:: https://img.shields.io/github/contributors/veit/flask-bokeh-dashboard.svg
   :target: https://github.com/veit/flask-bokeh-dashboard/graphs/contributors
.. |License| image:: https://img.shields.io/github/license/veit/flask-bokeh-dashboard.svg
   :target: https://github.com/veit/flask-bokeh-dashboard/blob/master/LICENSE

Features
========

The package provides a starter pack with an interactive `Bokeh
<https://bokeh.pydata.org>`_ plot embedded in a `Material Design
<https://material.io/>`_ Dashboard, which can send parameters from a flask form
to Bokeh.

.. image:: screenshot.png
   :scale: 53%
   :alt: Material Dashboard with Bokeh embedded in Flask

.. note::
   Please keep in mind that this is only a lightweight example of how Flask can
   affect the rendering of the bokeh plot. The change in scale is out of scope.

Quickstart
==========

Before you install Python packages, you must meet a few requirements.

#. Make sure you use the desired Python version:

   .. code-block:: console

    $ python3 -V
    Python 3.13.2

   Only Python >=3.9 is supported.

#. Install `uv <https://docs.astral.sh/uv/>`_:

   * … on macOS and Linux:

     .. code-block:: console

        $ curl -LsSf https://astral.sh/uv/install.sh | sh

   * … on Windows

     .. code-block:: ps1

        > powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

#. Download:

   .. code-block:: console

    $ curl -O https://github.com/veit/flask-bokeh-dashboard/archive/master.zip
    $ unzip master.zip

#. Create virtual environment:

   .. code-block:: console

    $ cd flask-bokeh-dashboard
    $ uv sync

#. Run the dashboard with the `gunicorn
   <http://docs.gunicorn.org/en/stable/run.html>`_ command:

   .. code-block:: console

    $ uv run gunicorn -w 1 main:app
    [2021-09-08 10:10:16 +0200] [55490] [INFO] Starting gunicorn 20.1.0
    [2021-09-08 10:10:16 +0200] [55490] [INFO] Listening at: http://127.0.0.1:8000 (55490)
    [2021-09-08 10:10:16 +0200] [55490] [INFO] Using worker: sync
    [2021-09-08 10:10:16 +0200] [55498] [INFO] Booting worker with pid: 55498

   .. note::
      The ``w`` option can be used to specify the number of workers.

#. Visit http://127.0.0.1:8000 and it should look like the screenshot above.

#. You can shut down the service in the console with ``ctrl-c``.

Pull requests
=============

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. I also accept pull requests on this, if they are
small, atomic, and if they make my own packaging experience better.
