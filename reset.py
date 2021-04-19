import os
import json

os.system("rm db.sqlite3")
os.system("touch db.sqlite3")

with open("core/setup_test/requirements.json", "w") as w:
    w.write(json.dumps({
        'token': ''
    }))

print("Reset has been successful")
