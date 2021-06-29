import redis
import click

@click.command()
@click.option('--days', default=7, help='Idle time limit to filter (default 7)')
@click.option('--size', default=300, help='Size key limit [Kb] (default 300Kb)')
@click.option('--data', default=False, help='It will dump also data contents if True, Key name and metadata only if False')
@click.option('--break_on', default=1000, help='Apply limit scan key (default 1000)')
def expire_keys(days, size, data, break_on):
    expire_days = days
    expire_seconds = expire_days * 24 * 60 * 60

    dump_count = 0

    size_limit_kb = size
    size_limit = size_limit_kb * 1024

    print(f"Scanning keys older than {expire_days} days, larger than {size_limit_kb} Kb")
    if data==True:
        print(f"ID;Size (kb);Idle (days);Key name;Data")
    else:
        print(f"ID;Size (kb);Idle (days);Key name")
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for i, key in enumerate(r.scan_iter("*")):
        ttl = r.ttl(key)
        size = r.memory_usage(key)
        if size >= size_limit:
            idle = r.object("idletime", key)
            if idle >= expire_seconds:
               key_name = key.decode('utf8')
               try:
                   key_data = r.get(key_name)
               except:
                   key_data = "No data!"
               dump_count = dump_count + 1
               if data==True:
                   print(f"{i};{(size / 1024):.3f};{(idle / 60 / 60 / 24):.3f};{key_name};{key_data}")
               else:
                   print(f"{i};{(size / 1024):.3f};{(idle / 60 / 60 / 24):.3f};{key_name}")

        if break_on and break_on <= i:
            break

    print(f"Scan completed, scanned/dumped {dump_count}/{i} keys")

if __name__=="__main__":
  expire_keys()
