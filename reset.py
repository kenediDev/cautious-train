import os
import json
import cowsay


command = """
from database.models.user import Location\n
from django.contrib.auth.models import User
user = User(username='Username',email='Email@yahoo.com',password='Password',is_superuser=True,is_staff=True)
user.set_password('Password')
user.save()
location = Location()
location.save()
user.accounts_set.create(location=location)
"""

with open("prefix/d_rst.data", "w") as w:
    w.write("Reset")

os.system("rm db.sqlite3")
os.system("touch db.sqlite3")
os.system("rm media/accounts/* && rm media/product/* && rm media/category/*")
os.system("python manage.py migrate")
os.system('python manage.py shell -c="%s"' % command)
os.system("export reset='True'")
os.system("python manage.py test")

with open("core/setup_test/requirements.json", "w") as w:
    w.write(json.dumps({
        'token': ''
    }))

_ = []
_.append("=" * 45)


cowsay.dragon(
    "The application reset was successful \n and then you can just run the command: \npython manage.py test \n Author: Kenedi Novriansyah \n Live at DIYogayakarta")
