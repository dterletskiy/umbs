FROM ubuntu:20.04

# Fix for tzdata for docker image build
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone

ARG ARG_PACKAGES=" \
   apt-utils cpio python python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping \
   python3-jinja2 libegl1-mesa pylint3 xterm \
   vim locales devscripts debhelper \
   gawk wget diffstat texinfo chrpath socat libsdl1.2-dev \
   python-crypto checkpolicy python3-git python3-github \
   bzr pigz m4 lftp openjdk-8-jdk git-core rsync \
   gnupg flex bison gperf build-essential zip curl zlib1g-dev \
   gcc-multilib g++-multilib libc6-dev-i386 lib32ncurses5-dev \
   x11proto-core-dev libx11-dev lib32z1-dev ccache libgl1-mesa-dev \
   libxml2-utils xsltproc unzip bc ninja-build python3-pygit2 \
   python3-pyelftools python3-crypto libncurses5 libssl-dev \
"

# Install necessary for build packages
RUN apt-get update && apt-get upgrade && apt install -y ${ARG_PACKAGES}

# Define name for user and uid/gid
ARG ARG_USER_NAME=guest
ARG ARG_USER_ID=1000
ARG ARG_USER_GID=1000
ARG ARG_USER_WORKDIR="workspace"

# Creating the user
RUN groupadd --gid ${ARG_USER_GID} ${ARG_USER_NAME} && \
   useradd \
      --uid ${ARG_USER_ID} \
      --gid ${ARG_USER_GID} \
      --create-home \
      --shell /bin/bash \
      ${ARG_USER_NAME}

# Switch the user from root to $ARG_USER_NAME
USER ${ARG_USER_NAME}
ENV USER_NAME=${ARG_USER_NAME}

# Create workdir for docker and define it as WORKDIR
RUN mkdir -p /home/${ARG_USER_NAME}/${ARG_USER_WORKDIR} && chown ${ARG_USER_NAME}:${ARG_USER_NAME} /home/${ARG_USER_NAME}/${ARG_USER_WORKDIR}
ENV BUILD_DIR /home/${ARG_USER_NAME}/${ARG_USER_WORKDIR}
WORKDIR ${BUILD_DIR}
ENV PATH ~/.local/bin:${PATH}
