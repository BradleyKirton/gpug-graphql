 ## GPUG Meetup June 30 2018

The slides that go along with this repository can be found [here](https://slides.com/bradleystuartkirton/deck-2/#/).

## Installation

This project makes use of pipenv. To install the dependencies first [install pipenv](https://docs.pipenv.org/#install-pipenv-today) and then run the following make file command.

```bash
make install
```

## Running services

To run the services make sure you have redis installed and run the following make command.

```bash
make run -j3
```

Note the superuser's authentication details are as follows:

- username: admin
- password: admin


If you wish to load additional meetups add an API key to the MEETUP_API_ENV_NAME env variable.