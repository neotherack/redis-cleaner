# Redis Cleaner for Alchemy

## Installation
1. Clone repo
2. Setup
```
python -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```
2. Run cleaner or expirer scripts
(see examples)


## Script usage

### Cleaner
```
python redis_cleaner.py --help
Usage: redis_cleaner.py [OPTIONS]

Options:
  --days INTEGER    Idle time limit to filter (default 7)
  --size INTEGER    Size key limit [Kb] (default 300Kb)
  --delete BOOLEAN  Delete if True, Report if False
  --help            Show this message and exit.
```


### Expirer
```
python redis_expirer.py --help
Usage: redis_expirer.py [OPTIONS]

Options:
  --days INTEGER      Idle time limit to filter (default 7)
  --size INTEGER      Size key limit [Kb] (default 300Kb)
  --expire BOOLEAN    Expire if True, Report if False
  --break_on INTEGER  Apply limit scan key (default 1000)
  --help              Show this message and exit.
```

## Parameter hints
"days" parameter will be used to compare agains "idle time" on the key
this value will get in sync anytime on read or write each key.

* "size" (kb) will be used to filter keys using more than that memory space

* "delete" / "expire": if True, it will apply changes, if not, it will just display info with no changes on the system

* "break_on", used to scan only the first N keys, just for debug/testing purposes. To perform a full scan use a huge value such as 1000000.


## Example commands
* Delete keys older than 7 days and larger than 650kb
```
python redis_cleaner.py --days=7 --size=650 --delete=True
```

* Report (not delete applied) keys older than 4 days and larger than 250kb
```
python redis_cleaner.py --days=4 --size=250 --delete=False
```

* Set TTL on the next 2 days for keys older than 2 days which are larger than 500kb 
**IMPORTANT! keys older than 2 days to be deleted in the next two days, so key will stay for 4 days in total**
```
python redis_expirer.py --days=2 --size=500 --delete=True
```

* Test run (won't set any key to expire) for keys older than 5 days larger than 250kb (note: it will only scan first 1000 keys only)
**IMPORTANT! it will produce CSV output**
```
python redis_expirer.py --days=5 --size=250 --delete=False --break_on=1000
```
