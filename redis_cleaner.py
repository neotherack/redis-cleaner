#!/usr/bin/env python
import redis

drop_limit_days = 90
drop_limit_seconds = drop_limit_days * 24 * 60 * 60

r = redis.StrictRedis(host='localhost', port=6379, db=0)
for key in r.scan_iter("*"):
    idle = r.object("idletime", key)
    if idle >= drop_limit_seconds:
        #r.delete(key)
        print(f"To drop key: {key}")

print(f"Process completed")
