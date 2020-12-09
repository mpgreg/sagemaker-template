#FROM python:3.6
FROM almondsh/almond:0.10.3-scala-2.13.3

WORKDIR /tmp
COPY ./requirements.txt ./conda-requirements.txt ./install.R ./startup.sh ./rserver.conf /tmp/

ARG NB_USER="sagemaker-user"
ARG NB_UID="1000"
ARG NB_GID="100"
ARG RSTUDIO_URL=https://s3.amazonaws.com/rstudio-ide-build/server/bionic/amd64/rstudio-server-1.4.1081-amd64.deb
ARG RSTUDIO_MD5=1fc43ed6a80cdb43f2231ac860751467
#ARG RSTUDIO_URL=https://download2.rstudio.org/server/bionic/amd64/rstudio-server-1.3.1093-amd64.deb
#ARG RSTUDIO_MD5=c364778cb79e3de2259c08e8d00eff01 

USER root

RUN \
    chmod u+x /tmp/startup.sh && \
    apt-get update && \
    apt-get install -y sudo && \
    #useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    #chmod g+w /etc/passwd && \
    usermod -l ${NB_USER} jovyan && \
    mv /home/jovyan /home/${NB_USER} && \
    usermod -d /home/${NB_USER} ${NB_USER} && \
    echo ${NB_USER}:sagemaker123 | /usr/sbin/chpasswd && \
    echo "${NB_USER}    ALL=(ALL)    NOPASSWD:    ALL" >> /etc/sudoers && \
    # Prevent apt-get cache from being persisted to this layer.
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Make the default shell bash (vs "sh") for a better Jupyter terminal UX
ENV SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    NB_GID=$NB_GID \
    RSTUDIO_WHICH_R=/opt/conda/bin/R \
    HOME=/home/$NB_USER 

USER $NB_UID

# R packages and Python packages that are usable via "reticulate".
RUN \
    conda install --quiet --yes --file /tmp/conda-requirements.txt && \
    /opt/conda/bin/Rscript /tmp/install.R && \
    pip install --quiet --no-cache-dir -r /tmp/requirements.txt && \
    conda clean --all -f -y

USER root

# Setup the "sagemaker-user" user and install R with requirements
RUN \
      apt-get update && \
      apt-get install -y --quiet --no-install-recommends \
      #fonts-dejavu \
      make \
      gcc \
      libclang-dev \
      psmisc \
      git \
      ssh \
      xz-utils \
      #vim \
      && \
      apt-get install -y --quiet gdebi-core && \
      curl -o /tmp/rstudio-installer.deb ${RSTUDIO_URL} && \
      echo "${RSTUDIO_MD5} /tmp/rstudio-installer.deb" | md5sum -c - && \
      gdebi --quiet --option=APT::Get::force-yes=1,APT::Get::Assume-Yes=1 -n /tmp/rstudio-installer.deb && \
      mv /tmp/rserver.conf /etc/rstudio/rserver.conf && \
      rm /tmp/rstudio-installer.deb 

WORKDIR $HOME
USER $NB_UID

ENTRYPOINT /tmp/startup.sh
