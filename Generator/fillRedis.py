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
iterations = 10

# Perform Redis operations
for i in tqdm(range(iterations), desc="Processing Redis commands"):
    # UUID and timestamp for key name
    key_uuid = str(uuid.uuid4())
    key_timestamp = str(int(time.time()))
    redis_connection.set(f"{key_uuid}_{key_timestamp}_json", json.dumps(json_data))
    redis_connection.set(f"{key_uuid}_{key_timestamp}_image_base64", image_data)
    # # Other Redis commands
    redis_connection.mset({f"{key_uuid}_key1": "value1", f"{key_uuid}_key2": "value2"})
    redis_connection.setnx(f"{key_uuid}_setnx_key", "value")
    redis_connection.setex(f"{key_uuid}_setex_key", 10, "value")
    redis_connection.psetex(f"{key_uuid}_psetex_key", 10000, "value")
    redis_connection.getset(f"{key_uuid}_getset_key", "new_value")
    redis_connection.hset(f"{key_uuid}_hash", "field", "value")
    redis_connection.hset(f"{key_uuid}_hash_multi", mapping={"field1": "value1", "field2": "value2"})
    redis_connection.hsetnx(f"{key_uuid}_hash_setnx", "field", "value")

    # # Create a list before using lset
    redis_connection.lpush(f"{key_uuid}_list", "initial_value")
    redis_connection.lset(f"{key_uuid}_list", 0, "value")

    redis_connection.lpush(f"{key_uuid}_list_push", "value")
    redis_connection.sadd(f"{key_uuid}_set", "value")
    redis_connection.zadd(f"{key_uuid}_zset", {"value": 1})
    redis_connection.pfadd(f"{key_uuid}_pfadd", "value")