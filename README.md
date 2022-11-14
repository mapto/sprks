Security Policy Risk Simulator (sprks)
======================================

[![Build Status](https://travis-ci.org/mapto/sprks.png)](https://travis-ci.org/mapto/sprks)


This is the website of the SPRKS project. It is an exploratory game employing agent-based simulation to represent the real-life complexities of corporate information security.

SPRKS is being developed at UCL Information Security Research Group and is supported by Intel and IBM.

A game overview can be seen in the [docs](docs/) directory. Check out the [wiki page](https://github.com/mapto/sprks/wiki) for technical details.

This project has been suspended due to lack of time.

# Installation

The game was developed in 2014 and uses legacy software. The simplest way to use it now is to use [docker-compose](https://docs.docker.com/compose/). This will install a development version. Once started, run tests with:

    docker exec -it sprks_app_1 /bin/bash -c "pip install pytest && cd app && py.test"