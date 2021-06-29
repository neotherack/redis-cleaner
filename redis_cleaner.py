import redis
import click

@click.command()
@click.option('--days', default=7, help='Idle time limit to filter (default 7)')
@click.option('--size', default=300, help='Size key limit [Kb] (default 300Kb)')
@click.option('--delete', default=False, help='Delete if True, Report if False')
def clean(days, size, delete):
    scanned=0
    dropped=0
    drop_limit_days = days
    drop_limit_seconds = drop_limit_days * 24 * 60 * 60

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for key in r.scan_iter("*"):
        scanned = scanned+1
        idle = r.object("idletime", key)
        mem = r.memory_usage(key)
        if idle >= drop_limit_seconds and mem>=size:
            if delete and delete==True:
                print(f"Dropped key: {key}")
                dropped=dropped+1
                r.delete(key)
            else:
                print(f"To drop key: {key}")

    print(f"Process completed, scanned {scanned} keys, dropped {dropped}")

if __name__ == '__main__':
    clean()
