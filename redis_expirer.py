import redis
import click

@click.command()
@click.option('--days', default=7, help='Idle time limit to filter (default 7)')
@click.option('--size', default=300, help='Size key limit [Kb] (default 300Kb)')
@click.option('--expire', default=False, help='Expire if True, Report if False')
@click.option('--break_on', default=1000, help='Apply limit scan key (default 1000)')
def expire_keys(days, size, expire, break_on):
    expire_days = days
    expire_seconds = expire_days * 24 * 60 * 60

    size_limit_kb = size
    size_limit = size_limit_kb * 1024
    size_sum=0

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
               if expire==True:
                   r.expire(key, expire_seconds)
               else:
                   print(f"{i};{(size / 1024):.2f};{(idle / 60 / 60 / 24):.2f};{key.decode('utf8')}")

        if break_on and break_on <= i:
            break

    print(f"Process completed, analyzed {i} keys")
    print(f"Memory excess {(size_sum / 1024):.2f} Kb | {(size_sum / 1024 / 1024):.2f} Mb")

if __name__=="__main__":
  expire_keys()
