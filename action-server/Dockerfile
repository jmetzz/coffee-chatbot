FROM centos:centos7

RUN yum -y update \
    && yum -y install curl bzip2 \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local/ \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3 \
    && conda update conda \
    && conda clean --all --yes \
    && rpm -e --nodeps curl bzip2 \
    && yum clean all \
    && echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
    && source /etc/profile.d/conda.sh

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LC_TYPE=en_US.UTF-8


COPY environment.yml .

RUN conda env create -f environment.yml && \
    conda clean --all --yes


SHELL [ "/bin/bash", "-c" ]
WORKDIR /app

COPY entrypoint.sh .
COPY src/main /app/src/main

#RUN chmod +x entrypoint.sh && \
#    /fix-permissions.sh /app

EXPOSE 5055

ENTRYPOINT ["./entrypoint.sh"]
CMD ["run"]
