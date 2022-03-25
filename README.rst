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

Data
-----
This project currently reads dat

Docker
-------
Build the image, we'll name it `my-image`.

.. code-block:: bash

    docker build -t my-image .


This may take a few minutes.

Instantiate and run the container, we'll map localhost:8080 to the application

.. code-block:: bash

    docker run --rm -p 8080:80 --volume $(pwd)/data/:/data/ stockviewer

Docker on ARM
--------------
Create a local registry

.. code-block:: bash

    docker run -d -p 5001:5000 -v registry_data:/var/lib/registry --restart=always --name registry registry:2

Build the image for AMD64 arch and push to the previously created registry

.. code-block:: bash

    docker buildx build --platform=linux/amd64 --tag localhost:5001/stockviewer:latest --output=type=registry,registry.insecure=true .

Pull the container from the registry and run (add `--pull=always` option to ensure pulling the newest version in
case of a code update)

.. code-block:: bash

    docker run --rm --platform=linux/amd64 -p 8000:80 --pull=always localhost:5001/stockviewer

