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


Development
-----------

The same container that runs locally for testing should run in production.
Configuration and secrets are provided to the container at runtime.
The application should not need to be aware of the environment it runs in.

### Dependency pinning

    rm -rf venv
    python3 -m venv venv && . venv/bin/activate
    pip-sync

Python dependencies are pinned using [pip-tools][]. The `requirements.in` file
lists the direct dependencies of the application with a version constraint
allowing minor and point release upgrades, but not major version upgrades.

It's probably most sensible to install `pip-tools` in your user-wise Python
packages, rather than inside each venv. (This recommendation may change.) All
the below commands should be run while the venv is activated, however.

To add a dependency, add a constrained requirement for it to `requirements.in`
and run `pip-compile`.

To upgrade all dependencies to new versions that match the `requirements.in`
constraints, run `pip-compile --upgrade`. (Eventually we may have a process do
this automatically and make pull requests.)

`pip-compile`'s output is a `requirements.txt` file, which should be committed
when it changes and never edited manually.

To install the pinned dependencies in `requirements.txt` into your venv, run
`pip-sync`.

[pip-tools]: https://github.com/jazzband/pip-tools


### Container build

    # open a tunnel to the database
    # if the app connects to more than one database cluster, you'll need
    # to forward a different local port to each one.
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
