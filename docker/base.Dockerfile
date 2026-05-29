# Shared base image for ESD cosmology replication studies.
# Each study builds a thin layer on top of this with its own
# pinned dependencies.
#
# Build:
#   docker build -f docker/base.Dockerfile -t esd-cosmology-base .

FROM python:3.11-slim

LABEL org.opencontainers.image.title="esd-cosmology-base"
LABEL org.opencontainers.image.description="Shared base image for ESD framework cosmology replication studies."
LABEL org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System dependencies needed by CLASS/CAMB/scientific Python stack.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        git \
        make \
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/esd-cosmology

# Install the shared esd_core library.
COPY pyproject.toml ./
COPY esd_core/ ./esd_core/
RUN pip install --upgrade pip setuptools wheel \
    && pip install -e .[test]

# Default workdir for studies that mount themselves at /work.
WORKDIR /work
CMD ["bash"]
