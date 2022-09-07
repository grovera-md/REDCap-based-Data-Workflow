import os
import time

for x in range(10):
    exec(open("initialize_sqlite_db.py").read())
    exec(open("redcap_to_sqlite.py").read())
    if x != 9:
        os.remove("redcap.db")
        time.sleep(10)
