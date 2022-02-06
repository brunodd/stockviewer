StockViewer
===========
This application is initially created to play around with

- python
- pandas
- basic visualizations
- encapsulation in Docker


Functionally, the goal is to have an application that can perform basic
reporting on an arbitrary stock portfolio.

Installation
------------
StockViewer uses the `poetry` dependency manager for development and deployment.

To run the application locally, run

.. code-block:: bash

    poetry run python -m app

To package the application and create the wheel file run

.. code-block:: bash

    poetry build

Docker
-------
Build the image, we'll name it `my-image`.

.. code-block:: bash

    docker build -t my-image .


This may take a few minutes.

Instantiate and run the container, we'll map localhost:8080 to the application

.. code-block:: bash

    docker run --rm -p 8080:80 my-image

