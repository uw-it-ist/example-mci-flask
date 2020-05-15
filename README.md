Example MCI Flask app
========

This is the example Flask app that is deployed to the MCI system.

Your app should provide documentation in the README.md file like this one.
Here is some guidance for writing good documentation:
- [Write the Docs](http://www.writethedocs.org/guide/writing/beginners-guide-to-docs/)
- [Documenting your projects on GitHub](https://guides.github.com/features/wikis/)


Getting started
---------------

- Setup your [development environment](https://wiki.cac.washington.edu/x/4fDFBg)
- Learn more [about MCI](https://wiki.cac.washington.edu/x/T3ZjBg)


Testing
-------

The same container that runs locally for testing should run in production.
Configuration and secrets are provided to the container at runtime.
The application should not need to be aware of the environment it runs in.

### Reproducible container building

Python dependencies can be pinned in the setup.py or a requirements.txt file.
During development you normally want to use the latest versions of dependencies so you can
clear the requirements.txt file and the docker-compose build will install the latest versions.
When you want to freeze the dependencies copy them to the requirements.txt file.

### Local Development

    rm -rf venv
    python3 -m venv venv && source venv/bin/activate
    python3 setup.py test
    pip install .
    pip freeze | grep -v $(python3 setup.py --name) > requirements.txt


### Local testing

    # open a tunnel to the database
    ssh -L 5432:mario-dev01:5432 bowser-dev01

    # build
    docker-compose build

    # run
    docker-compose up

    # serve
    curl http://127.0.0.1:8001/example-flask-app/healthz


Monitoring
----------

The "healthz" endpoint will test the code and report a status code.

    GET /example-flask-app/healthz

Gunicorn produces statsd metrics which are gathered by prometheus.

App specific metrics can also be emitted for prometheus.


Deployment
----------

Tag and push the container to the GCP Container Registry and Flux will auto deploy it.

    export GIT_REPO_NAME=example-flask-app
    gcloud --project uwit-mci-ist builds submit \
        --tag gcr.io/uwit-mci-ist/$GIT_REPO_NAME:$(git describe --always --tag) .


Roadmap and TODO
----------------
There is still stuff to do here:

- automatic deployment from github:
    build, tag and push container to registry, flux will do the rest
- require_weblogin_authentication might be better implemented as
    a shared library or an external service
- this could be further simplified to not use blueprints and look more like the
    typical tutorial apps in the flask documentation
- another example project could provide a pattern for a javascript/angular/jquery frontend
    with Flask as a backend API
- HTTP/2 support
- Asset bundling with flask_assets
