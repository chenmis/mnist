FROM python:3.9-slim-bullseye as build

# Install virtualenv
RUN pip install --no-input virtualenv

WORKDIR /code

COPY requirements.txt /code/
RUN python3 -m venv .venv

# Enter venv and install requirements
ENV PATH=/code/.venv/bin:$PATH
RUN pip install -r requirements.txt


ENV PROTOS_DIR=/code/protos
COPY protos/ ${PROTOS_DIR}/
RUN ${PROTOS_DIR}/compile_files.sh

FROM python:3.9-slim-bullseye

WORKDIR /code

# Copy the venv that was generated in the previous stage.
COPY --from=build /code/.venv /code/.venv
# Copy the code from outside the building cotext (excluding files in `.dockerignore`).
COPY . /code/
# Override the protos directory with the protos directory from the build stage (with the generated py files).
COPY --from=build /code/protos/ /code/protos/

# Prepend the venv bin path to PATH, mocking regular venv activate script.
ENV PATH=/code/.venv/bin:$PATH

# Define the image entrypoint, but use CMD to allow entrypoint override for easier debugging.
CMD /code/server_entrypoint.py
