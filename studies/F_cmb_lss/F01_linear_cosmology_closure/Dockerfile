# Thin layer over the shared esd-cosmology-base image.
#
# Build (from the study folder):
#   docker build -t esd-disco .
#
# Run (mount outputs back to host):
#   docker run --rm \
#     -v "$PWD/outputs:/work/outputs" \
#     -v "$PWD/figures_generated:/work/figures_generated" \
#     esd-disco make all

FROM esd-cosmology-base:latest

WORKDIR /work

# Study-specific dependencies.
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Study contents.
COPY Makefile ./
COPY scripts/ ./scripts/
COPY data/ ./data/

CMD ["make", "all"]
