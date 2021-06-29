import redis

expire_days = 4
expire_seconds = expire_days * 24 * 60 * 60

size_limit_kb = 100
size_limit = size_limit_kb * 1024
size_sum = 0

break_on = None

print(f"Scanning keys not used in the last {expire_days} days, larger than {size_limit_kb} Kb")
print(f"ID;Size (kb);Idle (days);Key name")

r = redis.StrictRedis(host='localhost', port=6379, db=0)
for i, key in enumerate(r.scan_iter("*")):
    ttl = r.ttl(key)
    size = r.memory_usage(key)
    if ttl == -1 and size >= size_limit:
        idle = r.object("idletime", key)
        size_sum = size_sum + size
        if idle >= expire_seconds:
            print(f"{i};{(size / 1024):.2f};{(idle / 60 / 60 / 24):.2f};{key.decode('utf8')}")
            #redis.expire(key, expire_seconds)

    if break_on and break_on <= i:
        break

print(f"Process completed, analyzed {i} keys")
print(f"Memory excess {(size_sum / 1024):.2f} Kb | {(size_sum / 1024 / 1024):.2f} Mb")