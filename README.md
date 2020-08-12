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

The development cycle looks something like this:

    git clone git@github.com:uw-it-ist/example-mci-flask
    cd example-mci-flask
    docker-compose up -d
    # -d makes your services run silently in the background, to tail logs:
    docker-compose logs -f app
    # visit localhost:8001/example-mci-flask in your browser!
    # hack some code and reload, docker-compose.yaml mounts your local code
    # into the running container and tells gunicorn to restart when files change

    # if you make some changes to the docker file, add a library to the
    # requirements, or you just feel like it
    docker-compose build app
    docker-compose restart app

### Dependency pinning

See the wiki for [instructions for dependency pinning][pinning].

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

- this could be further simplified to not use blueprints and look more like the
    typical tutorial apps in the flask documentation
- HTTP/2 support
- Asset bundling with flask_assets

[pinning]: https://wiki.cac.washington.edu/display/Tools/Dependency+pinning+for+Python+applications
