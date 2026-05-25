# Use the official AlmaLinux 9 base image
FROM almalinux:9

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install Python 3, pip, and curl (clean up the dnf cache immediately after)
RUN dnf update -y && dnf install -y \
    python3 \
    python3-pip

RUN dnf install -y --allowerasing curl

RUN dnf clean all

# Configure the NodeSource DNF repository for Node.js 20 and install nodejs (includes npm)
RUN curl -fsSL https://rpm.nodesource.com/setup_20.x | bash - \
    && dnf install -y nodejs \
    && dnf clean all

# Set up the working directory inside the container
WORKDIR /app

RUN curl -fsSL https://pi.dev/install.sh | sh
# RUN export PATH="/root/.local/share/pi-node/node-v22.22.3-linux-arm64/bin:$PATH"


# Default command to run when the container starts
CMD ["bash"]