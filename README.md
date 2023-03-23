# Mirror Redis Traffic to another redis node
<img src="https://raw.githubusercontent.com/alivx/redis-mirror/master/Generator/redis-mirror-logo.jpg" alt="logo" style="zoom:50%;" />


# redis-mirror
Realtime Redis Traffic Mirror to another instance, this script reads the STDOUT from the `redis-cli monitor` command and mirrors the keys to another instance.

## Use Case/Note
In some production/development cases, you need to mirror Redis traffic to another node to do some investigation or debugging.
* This script does not set `TTL` to mirrored key since you need it for debugging.
* The script support all command since it simply dump and restore the key as is.



## TO DO:
1. Add TTL as an option in mirrored redis instance, plus add an option to expand the origin `TTL`.
2. Support cluster to a single redis instance or vice versa.
3. Add an option to dump all keys name to the file for further analysis.
4. Add an option to get all keys from the source and migrate the keys to another redis instance.

## Option

```
redismirror --help
Usage: redismirror [OPTIONS]

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
redis-cli monitor | redismirror  --sport 6379 --shost localhost  --dhost 127.0.0.1 --dport 6379

#Exmaple 2
redis-cli monitor |  redismirror  --shost localhost --dport 6377  --limit 100
```

## Exmaple output:
```
$ redis-cli monitor | redismirror  --sport 6379 --shost localhost  --dhost 127.0.0.1 --dport 6378 --replace  --ttl --ttle 10 --limit 10

onnected to Redis: Host: localhost, Port: 6379, DB: 0
Connected to Redis: Host: 127.0.0.1, Port: 6378, DB: 0
✔  Mirrored key | Key: e2657ecd-6ee0-4182-9128-239be76cbba5_1679609769_json, TTL: 10, Status: OK - Command SET
☀  Skipping Key -> DUMP, Key -> e2657ecd-6ee0-4182-9128-239be76cbba5_1679609769_json
✔  Mirrored key | Key: e2657ecd-6ee0-4182-9128-239be76cbba5_1679609769_image_base64, TTL: 10, Status: OK - Command SET
☀  Skipping Key -> TTL, Key -> e2657ecd-6ee0-4182-9128-239be76cbba5_1679609769_json
✔  Mirrored key | Key: e2657ecd-6ee0-4182-9128-239be76cbba5_key1, TTL: 10, Status: OK - Command MSET
✔  Mirrored key | Key: e2657ecd-6ee0-4182-9128-239be76cbba5_setnx_key, TTL: 10, Status: OK - Command SETNX
✔  Mirrored key | Key: e2657ecd-6ee0-4182-9128-239be76cbba5_setex_key, TTL: 20, Status: OK - Command SETEX
☀  Skipping Key -> DUMP, Key -> e2657ecd-6ee0-4182-9128-239be76cbba5_1679609769_image_base64
✔  Mirrored key | Key: e2657ecd-6ee0-4182-9128-239be76cbba5_psetex_key, TTL: 20, Status: OK - Command PSETEX
☀  Skipping Key -> TTL, Key -> e2657ecd-6ee0-4182-9128-239be76cbba5_1679609769_image_base64
✔  Mirrored key | Key: e2657ecd-6ee0-4182-9128-239be76cbba5_getset_key, TTL: 10, Status: OK - Command GETSET
✔  Mirrored key | Key: e2657ecd-6ee0-4182-9128-239be76cbba5_hash, TTL: 10, Status: OK - Command HSET
✔  Mirrored key | Key: e2657ecd-6ee0-4182-9128-239be76cbba5_hash_multi, TTL: 10, Status: OK - Command HSET
✔  Mirrored key | Key: e2657ecd-6ee0-4182-9128-239be76cbba5_hash_setnx, TTL: 10, Status: OK - Command HSETNX
Limit reached: 10
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
Or
$ python3 -m venv env
then
$ source env/bin/activate
$ pip install -r requirements.txt

$ pip install setup.py

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
To Generate sample data for your test using the below command:
```Bash
cd tests/Generator/;bash SampleDataInserter.sh

# Or Using python script
# Make sure to update config in the same file
python fillRedis.py
```


The following commands are also not logged:

```
skip_commands_list = [
    'FLUSHDB', 'INFO', 'FLUSHALL', 'AUTH', 'QUIT', 'SELECT', 'CLIENT', 'ROLE',
    'BGREWRITEAOF', 'TIME', 'ECHO', 'CONFIG', 'MONITOR', 'SYNC', 'SHUTDOWN',
    'DBSIZE', 'DEBUG', 'COMMAND', 'SCRIPT', 'SAVE', 'OBJECT', 'SLAVEOF',
    'KEYS', 'BGSAVE', 'SCAN', 'DUMP', 'SLOWLOG', 'TTL', 'PING', 'LASTSAVE'
]
```

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
Benchmark results with MONITOR running (redis-cli monitor > /dev/null):
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
