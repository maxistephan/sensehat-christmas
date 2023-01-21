# FROM debian:buster-slim
FROM debian@sha256:98de137b613dfc97f6b1eaa2f2d0a167eec4c5b72e2a34fd215aa51c3dcc3a86

ARG HOST_UID
ARG HOST_GID
ARG HOST_GN

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt install -y locales && \
    localedef -i en_GB -c -f UTF-8 -A /usr/share/locale/locale.alias en_GB.UTF-8
ENV LANG=en_GB.utf8

RUN apt-get install --no-install-recommends -y \
    python3 python3-venv python3-all-dev python3-setuptools python3-pip

RUN apt-get install --no-install-recommends -y \
    sudo gosu gcc make \
    dpkg-dev devscripts equivs

RUN apt-get install --no-install-recommends -y \
    libcap2-bin apt-utils git-core

RUN pip3 install --upgrade pip

COPY docker-entrypoint /

RUN mkdir /builder

RUN groupadd --force --gid $HOST_GID $HOST_GN
RUN useradd -rm -d /builder/rpi-season-screen -s /bin/bash -g root -G sudo,$HOST_GN -u $HOST_UID -g $HOST_GID $HOST_GN

RUN echo "$HOST_GN ALL=NOPASSWD: ALL" > /etc/sudoers.d/rpi-season-screen-nopasswd && \
    chmod 660 /etc/sudoers.d/rpi-season-screen-nopasswd

USER $HOST_GN

WORKDIR /builder/rpi-season-screen

ENTRYPOINT ["/docker-entrypoint"]
