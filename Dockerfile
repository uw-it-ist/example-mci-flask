# Set up the basics
FROM python:3.8-slim AS build-stage

# now do everything as toolop
RUN adduser toolop --gecos "" --disabled-password
RUN mkdir -p /home/toolop/app && chown -R toolop:toolop /home/toolop
USER toolop

# add the app source
WORKDIR /home/toolop
COPY . app

RUN python3 -m venv venv

# activate the venv
ENV PATH="/home/toolop/venv/bin:$PATH"

# run tests with tox
FROM build-stage AS test

# run unit tests
WORKDIR /home/toolop/app
RUN pip install tox
RUN tox

# discard the test stage and actually run in production
FROM build-stage AS deploy-stage

WORKDIR /home/toolop/app
RUN pip install pip-tools

# install production dependencies
RUN pip-sync

# open the container port where the flask app listens
EXPOSE 8000

# start the executable
ENTRYPOINT ["gunicorn",  "flask_app.app:load()"]

# default parameters that can be overridden with: docker run <image> new params
CMD ["-b", ":8000", "--access-logfile", "-", "--log-level", "INFO"]
