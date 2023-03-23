import sys
import re
import redis
import click


# Set up command line options
@click.command()
@click.option("--shost", type=str, default="127.0.0.1", help="Source redis host/IP.")
@click.option("--sport", type=int, default=6379, help="Source redis port.")
@click.option("--sdb", type=int, default="0", required=False, help="Source redis DB.")
@click.option("--sauth", default=None, type=str, required=False, help="Source redis auth info.")
@click.option("--dhost", type=str, default="127.0.0.1", help="Destination redis host/IP.")
@click.option("--dport", type=int, default=6377, help="Destination redis port.")
@click.option("--ddb", type=int, default="0", required=False, help="Destination redis DB.")
@click.option( "--dauth", default=None, type=str, required=False, help="Destination redis auth info.")
@click.option("--limit", type=int, help="Stop mirror process at limit X.")
@click.option("--replace", type=bool, is_flag=True, default=False, help="Replace key if exists.")
@click.option("--ttl", type=bool, is_flag=True, default=False, help="Enable to mirrored the TTL value for each key if exist")
@click.option("--ttle", type=int, default=-1, help="Increase the TTL value of the key with custom value.")


def main(shost, sport, sdb, sauth, dhost, dport, ddb, dauth, limit, replace, ttl, ttle):
    """
    Main function that connects to the source and destination Redis instances, then starts mirroring keys
    based on the specified command line options.
    """
    source = make_connection(shost, sport, sdb, sauth)
    destination = make_connection(dhost, dport, ddb, dauth)
    get_stdout(source, destination, limit, replace, ttl, ttle)


skip_commands_list = [
    'FLUSHDB', 'INFO', 'FLUSHALL', 'AUTH', 'QUIT', 'SELECT', 'CLIENT', 'ROLE',
    'BGREWRITEAOF', 'TIME', 'ECHO', 'CONFIG', 'MONITOR', 'SYNC', 'SHUTDOWN',
    'DBSIZE', 'DEBUG', 'COMMAND', 'SCRIPT', 'SAVE', 'OBJECT', 'SLAVEOF',
    'KEYS', 'BGSAVE', 'SCAN', 'DUMP', 'SLOWLOG', 'TTL', 'PING', 'LASTSAVE'
]


def make_connection(host, port, db, auth):
    """
    Create a connection to a Redis instance with the specified host, port, DB, and authentication.
    """
    # Create a connection pool
    pool = redis.ConnectionPool(
        host=host, port=port, db=db,
        password=auth) if auth else redis.ConnectionPool(host=host, port=port, db=db)
    r = redis.StrictRedis(connection_pool=pool)

    # Test connection
    try:
        r.ping()
        print(f"Connected to Redis: Host: {host}, Port: {port}, DB: {db}")
    except Exception as e:
        print(f"Redis connection error: ({e})")
        sys.exit(1)

    return r


def split(delimiters, data, maxsplit=0):
    """
    Split the input data based on the specified delimiters and maxsplit.
    """
    try:
        regex_pattern = "|".join(map(re.escape, delimiters))
        data = re.split(regex_pattern, data, maxsplit)
        command = data[1]
        data = data[3]
        return data, command
    except Exception as e:
        return None, None


def stdin_stream(timeout=0.5):
    """Get STDIN

    Returns:
        _io.TextIOWrapper: STDIN stream
    """
    if not sys.stdin.isatty():
        input_stream = sys.stdin
    else:
        print("There is no stdin, check help for more info. exit 1")
        sys.exit(1)
    return input_stream


def get_stdout(source_conn, dest_conn, limit, replace, ttl, ttle):
    """
    Read keys from the source Redis instance and mirror them to the destination Redis instance,
    based on the specified options.
    """
    counter = 0

    for line in stdin_stream():
        key, command = split('"', line, 5)
        if command in skip_commands_list:
            print(f"☀  Skipping Key -> {command}, Key -> {key}")
        elif key is not None and '] "DUMP" "' not in line:
            counter += 1
            data = source_conn.dump(key)
            key_original_ttl = source_conn.ttl(key)
            if ttl and key_original_ttl > 0:
                key_ttl = ttle + key_original_ttl
            else:
                key_ttl = ttle
            try:
                if command == "psetex":
                    print("command is psetex")
                    data = str(data).encode('utf-8')
                    return_val = dest_conn.psetex(name=key, time_ms=key_ttl, value=data)
                return_val = dest_conn.restore(name=key, ttl=key_ttl, value=data, replace=replace)
                if key_ttl > 0:
                    dest_conn.expire(key, key_ttl)
                print(
                    f"✔  Mirrored key | Key: {key}, TTL: {key_ttl}, Status: {return_val.decode('utf-8')} - Command",
                    command)
            except Exception as e:
                print(f"Skipping operation '{key}' due to error: {e}")
            if counter == limit:
                print(f"Limit reached: {counter}")
                sys.exit(0)


if __name__ == "__main__":
    main()