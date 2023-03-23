#Option
numberOfInsert=${1:-100}
insertSleepTime=${2:-0.1}

for i in $(seq 1 "${numberOfInsert}"); do
    key1=$(uuidgen)
    key2=$(date +"%s")
    key3=$(date)
    key4=$(cat Sample.json)
    key5=$(cat image.png.base64)
    redis-cli set "${key1}_${i}_uuid_ran" "$key1"
    redis-cli EXPIRE  "${key1}_${i}_uuid_ran" 20
    redis-cli set "${key1}_${i}_date_ran" "$key2"
    redis-cli EXPIRE  "${key1}_${i}_date_ran" 20
    redis-cli set "${key1}_${i}_date2_ran" "$key3"
    redis-cli EXPIRE  "${key1}_${i}_date2_ran" 20
    redis-cli set "${key1}_${i}_json_ran" "$key4"
    redis-cli EXPIRE  "${key1}_${i}_json_ran" 20
    # redis-cli set "${key1}_${i}_image_ran" $key5

    redis-cli hset ${key2}_${i}_uuid_ran ${i} "$key1"
    redis-cli hset ${key2}_${i}_date_ran ${i} "$key2"
    redis-cli hset ${key2}_${i}_date2_ran ${i} "$key3"
    redis-cli hset ${key2}_${i}_json_ran  $i "$key4"
    # redis-cli hset ${key2}_${i}_image_ran $i $key5
    sleep "$insertSleepTime"
    echo "$key1     $key2     $key3"
done
