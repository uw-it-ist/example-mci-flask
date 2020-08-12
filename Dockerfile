# Set up the basics
FROM python:3.8-slim AS base-stage

# now do everything as toolop
RUN adduser toolop --gecos "" --disabled-password
RUN mkdir -p /home/toolop/app && chown -R toolop:toolop /home/toolop
USER toolop
WORKDIR /home/toolop

# Set up an empty venv
RUN python3 -m venv venv
ENV PATH="/home/toolop/venv/bin:$PATH"

# Add the python requirements file to the container in a separate step to
# take better advantage of layer caching. requirements.txt, and thus the
# dependency closure, changes infrequently, so we can rebuild our containers
# in development faster if we make sure dependencies are cached in image layers
# that don't get invalidated when other parts of the app change.
COPY ./requirements.txt app/

# run tests with tox
FROM base-stage AS test-stage

RUN pip install tox

WORKDIR /home/toolop/app
COPY . .

RUN tox

# discard the test stage and actually run in production
FROM base-stage AS deploy-stage

WORKDIR /home/toolop/app

# Install production dependencies. Doing this before copying the app ensures
# that we don't have to rebuild this layer when the requirements haven't
# changed.
RUN pip install -r requirements.txt

WORKDIR /home/toolop/app
COPY --from=test-stage /home/toolop/app/flask_app /home/toolop/app/flask_app

# open the container port where the flask app listens
EXPOSE 8000

# start the executable
ENTRYPOINT ["gunicorn",  "flask_app.app:load()"]

# default parameters that can be overridden with: docker run <image> new params
CMD ["-b", ":8000", "--access-logfile", "-", "--log-level", "INFO"]
