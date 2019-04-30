
Install
-------

::

    # clone the repository
    $ git clone https://github.com/DenysTT/revolut_api.git


Build
-----

::

    # build docker image
    $ make build release=latest


Push
----

::

    # push docker image to repository
    $ make push release=latest

Run
---

::

    # to run locally (Dockerfile will be used)
    $ docker-compose up -d
    # to run on the cloud (image from the repo will be used in this case)
    $ docker-compose -f docker-compose-remote.yml

Open http://127.0.0.1:5000 in a browser.


Tests
----

::

    # run the following command to trigger tests
    $ docker exec -it revolut_api_app_1 pytest
