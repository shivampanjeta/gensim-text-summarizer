FROM ubuntu

WORKDIR /src
COPY . /src
RUN pip3 install gensim
RUN cd /src

CMD ['python3', '-m', 'http.server', '8000']
