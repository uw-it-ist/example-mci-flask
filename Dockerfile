# build and test the app in the first stage
FROM python:3.8-slim AS build-stage

# now do everything as toolop
RUN adduser toolop --gecos "" --disabled-password
RUN mkdir -p /home/toolop/app && chown -R toolop:toolop /home/toolop
USER toolop

# add the app source
WORKDIR /home/toolop
COPY . app

# activate the venv
ENV PATH="/home/toolop/venv/bin:$PATH"

# run unit tests
RUN python3 -m venv venv
WORKDIR /home/toolop/app
RUN pip install tox
RUN tox

# rebuild the venv that will stay in the container
WORKDIR /home/toolop
RUN rm -rf venv; python3 -m venv venv
WORKDIR /home/toolop/app

# install pinned requirements
# during development keep this file empty so you automatically get the latest versions
RUN pip install -r requirements.txt

# install the app to the venv
RUN pip install -q .

# show what can be put in requirements.txt to pin dependencies for future container builds
RUN echo "save to requirements.txt to pin dependencies" && pip freeze | grep -v $(python3 setup.py --name)

# discard the first stage and start again for the final image
# base docker image
FROM python:3.8-slim

# create a user so we don't run as root
RUN adduser toolop --gecos "" --disabled-password
USER toolop
WORKDIR /home/toolop

# install everything built in the first stage
COPY --from=build-stage /home/toolop/venv /home/toolop/venv

# open the container port where the flask app listens
EXPOSE 8000

# start the executable
ENTRYPOINT ["/home/toolop/venv/bin/gunicorn", "flask_app.app:load()"]

# default parameters that can be overridden with: docker run <image> new params
CMD ["-b", ":8000", "--access-logfile", "-", "--log-level", "INFO"]
