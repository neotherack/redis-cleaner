import redis
import click

@click.command()
@click.option('--days', default=7, help='Idle time limit to filter (default 7)')
@click.option('--size', default=300, help='Size key limit [Kb] (default 300Kb)')
@click.option('--delete', default=False, help='Delete if True, Report if False')
def clean(days, size, delete):
    scanned = 0
    dropped = 0
    mem_saved = 0
    drop_limit_days = days
    drop_limit_seconds = drop_limit_days * 24 * 60 * 60

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for key in r.scan_iter("*"):
        scanned = scanned+1
        idle = r.object("idletime", key)
        idle_days = idle / 3600 / 24
        mem = r.memory_usage(key)
        mem_kb = mem / 1024
        if idle >= drop_limit_seconds and mem_kb>=size:
            if delete and delete==True:
                print(f"Dropped key: idle:{idle_days:.3f} mem:{mem_kb:.2f} - {key.decode('utf8')}")
                dropped=dropped+1
                mem_saved = mem_saved + mem_kb
                r.delete(key)
            else:
                print(f"To drop key: {key}")

    print(f"Process completed, scanned {scanned} keys, dropped {dropped}. Saved {mem_saved} Kb")

if __name__ == '__main__':
    clean()
