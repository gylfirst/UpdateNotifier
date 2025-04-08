# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# If platform is arm then we add the piwheels index for prebuilt arm wheels
RUN if [ $(uname -m | cut -c 1-3) = "arm" ]; then \
    echo -e "[global]\nextra-index-url=https://www.piwheels.org/simple" > /usr/local/pip.conf; fi && \
    pip --no-cache-dir install -r requirements.txt --prefer-binary && \
    pip --no-cache-dir install -U setuptools

# Run the app
CMD [ "python3", "-m", "UpdateNotifier" ]
