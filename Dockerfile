# pull official base image
FROM python:3.9-slim

# set work directory
RUN mkdir /code
WORKDIR /code

# install psycopg2 dependencies
RUN apt-get update \
  && apt-get -y --no-install-recommends install \
     gcc g++ curl gettext vim git \
     # python depencies
     python3-dev python3-setuptools cython \
     # Pandas dependcies
     libblas3 libblas-dev liblapack3 liblapack-dev gfortran \
     # turicreate deps
     libgconf-2-4 \
     # Postgres
     libpq-dev \
     # Geoip Database
     libmaxminddb0 libmaxminddb-dev mmdb-bin \
  && apt-get clean

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry

# copy project
COPY ./poetry.lock /code/
COPY ./pyproject.toml /code/
RUN poetry config virtualenvs.create false --local
RUN poetry install
RUN pip install gunicorn
COPY . /code/
