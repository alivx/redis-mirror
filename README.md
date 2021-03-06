# Mirror Redis Traffic to another redis node
<img src="https://raw.githubusercontent.com/alivx/redis-mirror/master/Generator/redis-mirror-logo.jpg" alt="logo" style="zoom:50%;" />


# redis-mirror
Realtime Redis Traffic Mirror to another instance, this script reads the STDOUT from `redis-cli monitor` command and mirrors the keys to another instance.

## Use Case/Note
In some production/development cases, you need to mirror Redis traffic to another node in order to do some investigation or debugging.
* This script does not set `TTL` to mirrored key since you need it for debugging.
* The script support all command since it's simply dump and restore the key as is.



## TO DO:
1. Add TTL as an option in mirrored redis instance, plus add an option to expand the origin `TTL`.
2. Support cluster to a single redis instance or vice versa.
3. Add option to dump all keys name to file for further analysis.
4. Add option to get all keys from source and migrate the keys to another redis instance.

## Option

```
redismirror --help
Usage: redismirror [OPTIONS]

  The main function

  Args:     shost (str): source redis host     sport (int): source redis
  port     sdb (int): source redis database number     sauth (str): source
  redis auth info     dhost (str): destination redis host     dport (int):
  destination redis port     ddb (int): destination redis database number
  dauth (str): destination redis auth info     limit (int): number of
  iterations to stop script on it     replace (bool): replace key if exists

Options:
  --shost TEXT     Source redis host/IP.
  --sport INTEGER  Source redis port.
  --sdb INTEGER    Source redis DB.
  --sauth TEXT     Source redis auth info.
  --dhost TEXT     Destination redis host/IP.
  --dport INTEGER  Destination redis port.
  --ddb INTEGER    Destination redis DB.
  --dauth TEXT     Destination redis auth info.
  --limit INTEGER  Stop mirror process at limit X.
  --replace        Replace key if exists.
  --help           Show this message and exit.
```


## Useages
```Bash
redis-cli monitor | redismirror  --sport 6379 --shost localhost  --shost 10.0.1.51 --sport 6379

#Exmaple 2
redis-cli monitor |  redismirror  --shost localhost --dport 6377  --linit 100
```

## Exmaple output:
```
$ redis-cli monitor | redismirror  --shost localhost --dhost localhost --sport 6379 --dport 6377 --replace
Redis is connected, Host; localhost, Port:6379, DB:0
Redis is connected, Host; localhost, Port:6377, DB:0
Mirrored key | myhash
Mirrored key | myhash
Mirrored key | c75fdd21-9a50-4b43-87e6-44c86a8d1f78_1_uuid_ran
Mirrored key | c75fdd21-9a50-4b43-87e6-44c86a8d1f78_1_date_ran
Mirrored key | c75fdd21-9a50-4b43-87e6-44c86a8d1f78_1_date2_ran
Mirrored key | c75fdd21-9a50-4b43-87e6-44c86a8d1f78_1_json_ran
Mirrored key | c75fdd21-9a50-4b43-87e6-44c86a8d1f78_1_image_ran
Mirrored key | 1609966494_1_uuid_ran
Mirrored key | 1609966494_1_date_ran
Mirrored key | 1609966494_1_date2_ran
```

## Installation using pypi
```
pip install redismirror
```

## Installation

```
$ pip install -r requirements.txt

$ pip install setup.py
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run redismirror cli application

$ redismirror --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Redis Mirror `,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it redismirror --help
```



## Extra
To Generate sample data for your test use the below command:
```Bash
cd tests/Generator/;bash SampleDataInserter.sh
```


The following commands are also not logged:

* AUTH
* EXEC
* HELLO
* QUIT


Cost of running MONITOR
Because MONITOR streams back all commands, its use comes at a cost. The following (totally unscientific) benchmark numbers illustrate what the cost of running MONITOR can be.

Benchmark result without MONITOR running:


```Bash
$ src/redis-benchmark -c 10 -n 100000 -q
PING_INLINE: 101936.80 requests per second
PING_BULK: 102880.66 requests per second
SET: 95419.85 requests per second
GET: 104275.29 requests per second
INCR: 93283.58 requests per second
```
Benchmark result with MONITOR running (redis-cli monitor > /dev/null):
```Bash
$ src/redis-benchmark -c 10 -n 100000 -q
PING_INLINE: 58479.53 requests per second
PING_BULK: 59136.61 requests per second
SET: 41823.50 requests per second
GET: 45330.91 requests per second
INCR: 41771.09 requests per second
```
In this particular case, running a single MONITOR client can reduce the throughput by more than 50%. Running more MONITOR clients will reduce throughput even more.


License
-------

 GNU GENERAL PUBLIC LICENSE

Author Information
------------------

The tool was originally developed by [Ali Saleh Baker](https://www.linkedin.com/in/alivx/).
