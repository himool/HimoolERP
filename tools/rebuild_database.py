from django.core.wsgi import get_wsgi_application
from pathlib import Path
import pymysql
import sys
import os

host = '127.0.0.1'
user = 'root'
password = '123456'
database = 'oms'
project_path = Path.cwd()

# 重建数据库
print('重建数据库')
db = pymysql.connect(host=host, user=user, password=password)
cursor = db.cursor()
cursor.execute(f'DROP DATABASE {database};')
db.commit()
cursor.execute(f'CREATE DATABASE {database};')
db.commit()
cursor.close()
db.close()

# 删除 migrations 文件
print('删除 migrations 文件')
for app in (project_path / 'apps').iterdir():
    if app.is_file() or not (app / 'migrations').exists():
        continue

    for file in (app / 'migrations').iterdir():
        if file.is_file() and file.name != '__init__.py':
            file.unlink()

# Python3 manage.py
print('Python3 manage.py')
os.chdir(project_path)
os.system('python3 manage.py makemigrations && python3 manage.py migrate')
