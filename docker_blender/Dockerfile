# FROM public.ecr.aws/docker/library/ubuntu:22.04
# FROM public.ecr.aws/genophore/nvidia/cuda:12.3.1-runtime-ubuntu22.04
FROM public.ecr.aws/p4z0j1o0/nvidia:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN echo 'tzdata tzdata/Areas select Etc' | debconf-set-selections
RUN echo 'tzdata tzdata/Zones/Etc select UTC' | debconf-set-selections

ARG BLENDER_VERSION=${BLENDER_VERSION}
ARG BLENDER_VERSION_MAJOR=${BLENDER_VERSION_MAJOR}
ENV BLENDER_URL https://mirror.clarkson.edu/blender/release/Blender${BLENDER_VERSION}/blender-${BLENDER_VERSION_MAJOR}-linux-x64.tar.xz

# Install dependencies
RUN apt-get update -y && \
    apt-get install -y \
    sudo \
    curl \
    ca-certificates \
    zip \
    xz-utils \
    imagemagick \
    python3 \
    python3-pip \
    python3-pil \
    python3-pil.imagetk \
    xvfb \
    libnvidia-gl-515 \
    tree \
    libx11-dev \
    libxi-dev \
    libxxf86vm-dev \
    libfontconfig1 \
    libxrender1 \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    libsm6 \
    libwayland-client0 \
    libwayland-server0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN curl "${BLENDER_URL}" -o "blender.tar.xz" && \
    tar -xvf blender.tar.xz --strip-components=1 -C /bin && \
    rm -rf blender.tar.xz && \
    rm -rf blender

RUN pip3 install boto3 requests Wand

# EFS ENV
ENV EFS_BLENDER_FOLDER_PATH=/mnt/efs/projects

# Blender ENV
ENV BLENDER_EXECUTABLE=/usr/bin/blender

# Job Action type
# ENV JOB_ACTION_TYPE=render

# Copy specific folders and their contents
COPY ./app /app

# Give execute permissions to the script
RUN chmod +x /app/app.py

WORKDIR /app

ENV PYTHONPATH=/app:/mnt/efs/projects:$PYTHONPATH


ENTRYPOINT ["python3", "/app/app.py"]
