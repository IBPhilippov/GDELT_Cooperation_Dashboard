FROM mageai/mageai:latest

ARG USER_CODE_PATH
ARG PROJECT_NAME
ARG GOOGLE_CREDENTIALS
# Add Debian Bullseye repository
RUN echo 'deb http://deb.debian.org/debian bullseye main' > /etc/apt/sources.list.d/bullseye.list

# Install OpenJDK 11
RUN apt-get update -y && \
    apt-get install -y openjdk-11-jdk

# Remove Debian Bullseye repository
RUN rm /etc/apt/sources.list.d/bullseye.list

RUN pip3 install pyspark

ENV MAGE_DATA_DIR=
ENV USER_CODE_PATH=${USER_CODE_PATH}






