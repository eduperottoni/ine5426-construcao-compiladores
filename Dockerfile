# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables for non-interactive installations
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install gcc
RUN apt-get update && apt-get install -y gcc make

# Set the working directory inside the container
WORKDIR /app

# Command to run bash by default (you can override this)
CMD ["/bin/bash"]