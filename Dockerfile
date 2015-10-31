FROM kbase/depl:latest
MAINTAINER KBase Developer
# Install the SDK (should go away eventually)
RUN \
  . /kb/dev_container/user-env.sh && \
  cd /kb/dev_container/modules && \
  rm -rf jars && \
  git clone https://github.com/kbase/jars && \
  rm -rf kb_sdk && \
  git clone https://github.com/kbase/kb_sdk -b develop && \
  cd /kb/dev_container/modules/jars && \
  make deploy && \
  cd /kb/dev_container/modules/kb_sdk && \
  make


# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update

RUN mkdir -p /tmp/muscle


# --- {{
# WORKDIR /tmp/muscle
# ADD http://www.drive5.com/muscle/downloads3.8.31/muscle3.8.31_src.tar.gz ./muscle3.8.31_src.tar.gz
# RUN tar xzfp muscle3.8.31_src.tar.gz
# WORKDIR /tmp/muscle/muscle3.8.31/src 
# RUN make
# RUN mkdir -p /kb/runtime/muscle
# RUN cp /tmp/muscle/muscle3.8.31/src/muscle /kb/runtime/muscle/muscle

# -- I have:
#   [91mmake: execvp: ./mk: Text file busy
#   [91mmake: *** [muscle] Error 127
# --- }}


WORKDIR /tmp/muscle
ADD http://www.drive5.com/muscle/downloads3.8.31/muscle3.8.31_i86linux64.tar.gz ./muscle3.8.31_i86linux64.tar.gz
RUN tar xzfp muscle3.8.31_i86linux64.tar.gz
RUN mkdir -p /kb/runtime/muscle
RUN cp /tmp/muscle/muscle3.8.31_i86linux64 /kb/runtime/muscle/muscle3.8.31_i86linux64


RUN ln -s /kb/runtime/muscle/muscle3.8.31_i86linux64 /kb/runtime/bin/muscle
RUN rm -rf /tmp/muscle/*

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
ENV PATH=$PATH:/kb/dev_container/modules/kb_sdk/bin

WORKDIR /kb/module

RUN make

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]