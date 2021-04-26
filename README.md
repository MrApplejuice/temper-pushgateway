# temper-pushgateway

Tiny script to allow pushing metrics from a TEMPer USB temperature sensor to a prometheus pushgateway.

# How to install:

- Have Python 3.8 + pip installed
- Checkout repository
- Install pipenv: `pip install pipenv`
- Install pipenv environment: `pipenv install`
- Run temper monitor: `pipenv run python poll.py DIAG_data_center_lugia https://my-example-prometheus-server-.com:9091/ --username [authentication] --password [authentication]`

To run this in some userspace as a service, you can use this one-liner for crontab:

`flock -n service/started/lockfile  pipenv run python poll.py ...`
