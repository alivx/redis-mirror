import redis
import json
import base64
import uuid
import time
from tqdm import tqdm

# Load file contents
with open("Sample.json", "r") as json_file:
    json_data = json.load(json_file)

with open("image.png.base64", "rb") as image_file:
    image_data = base64.b64decode(image_file.read())

# Establish connection with Redis
redis_connection = redis.StrictRedis(host="localhost", port=6379, db=0)



# Config value for iteration
iterations = 1
sleepTime=0

# Perform Redis operations
for i in tqdm(range(iterations), desc="Processing Redis commands"):
    # UUID and timestamp for key name
    key_uuid = str(uuid.uuid4())
    key_timestamp = str(int(time.time()))
    redis_connection.set(f"{key_uuid}_{key_timestamp}_json", json.dumps(json_data))
    time.sleep(sleepTime)
    redis_connection.set(f"{key_uuid}_{key_timestamp}_image_base64", image_data)
    time.sleep(sleepTime)
    # # Other Redis commands
    redis_connection.mset({f"{key_uuid}_key1": "value1", f"{key_uuid}_key2": "value2"})
    time.sleep(sleepTime)
    redis_connection.setnx(f"{key_uuid}_setnx_key", "value")
    time.sleep(sleepTime)
    redis_connection.setex(f"{key_uuid}_setex_key", 10, "value")
    time.sleep(sleepTime)
    redis_connection.psetex(f"{key_uuid}_psetex_key", 10000, "value")
    time.sleep(sleepTime)
    redis_connection.getset(f"{key_uuid}_getset_key", "new_value")
    time.sleep(sleepTime)
    redis_connection.hset(f"{key_uuid}_hash", "field", "value")
    time.sleep(sleepTime)
    redis_connection.hset(f"{key_uuid}_hash_multi", mapping={"field1": "value1", "field2": "value2"})
    time.sleep(sleepTime)
    redis_connection.hsetnx(f"{key_uuid}_hash_setnx", "field", "value")
    time.sleep(sleepTime)

    # # Create a list before using lset
    redis_connection.lpush(f"{key_uuid}_list", "initial_value")
    time.sleep(sleepTime)
    redis_connection.lset(f"{key_uuid}_list", 0, "value")
    time.sleep(sleepTime)

    redis_connection.lpush(f"{key_uuid}_list_push", "value")
    time.sleep(sleepTime)
    redis_connection.sadd(f"{key_uuid}_set", "value")
    time.sleep(sleepTime)
    redis_connection.zadd(f"{key_uuid}_zset", {"value": 1})
    time.sleep(sleepTime)
    redis_connection.pfadd(f"{key_uuid}_pfadd", "value")
    time.sleep(sleepTime)
    redis_connection.geoadd(f"{key_uuid}_geoadd", 0, 0, "location")
    time.sleep(sleepTime)
    time.sleep(sleepTime)