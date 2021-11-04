from pathlib import Path

BASE_DIR = Path.cwd()


def run():
    create_nginx_config()
    create_database_config()
    create_uwsgi_config()


def create_nginx_config():
    is_need_create = input('是否需要创建 Nginx 配置文件吗? (y/n)\n')
    if is_need_create == 'y':
        listen_port = input('请输入 Nginx 监听端口:\n')
        server_port = input('请输入 Django 启动端口:\n')
        static_path = BASE_DIR / 'frontend/dist/'

        with open('/etc/nginx/sites-enabled/default', 'w') as file:
            file.write(f"""
server {{
    listen {listen_port};
    charset utf-8;
    gzip_static on;

	location / {{
		root {static_path};
		index index.html index.html;
		try_files $uri $uri/ /index.html;
	}}

	location /api/ {{
		proxy_pass http://localhost:{server_port}/api/;
		proxy_set_header Host $http_host;
		proxy_set_header X-Forwarded-Proto $scheme;
	}}

	location /media/ {{
		proxy_pass http://localhost:{server_port}/media/;
		proxy_set_header Host $http_host;
		proxy_set_header X-Forwarded-Proto $scheme;
	}}
}}
""")


def create_database_config():
    is_need_create = input('是否需要创建 数据库 配置文件吗? (y/n)\n')
    if is_need_create == 'y':
        database_type = input('配置数据库: (sqlite: 0, mysql: 1)\n')
        if database_type == '1':
            host = input('请输入 host:\n')
            user = input('请输入 user:\n')
            passowrd = input('请输入 passowrd:\n')
            database_name = input('请输入 数据库名称:\n')

            text = f"""
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '{host}',
        'PORT': '3306',
        'USER': '{user}',
        'PASSWORD': '{passowrd}',
        'NAME': '{database_name}',
        'OPTIONS': {{'charset': 'utf8mb4'}},
    }}
}}
"""
        else:
            text = f"""
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}
"""
        with open(BASE_DIR / 'configs/database.py', 'w') as file:
            file.write(text)


def create_uwsgi_config():
    is_need_create = input('是否需要创建 uwsgi 配置文件吗? (y/n)\n')
    if is_need_create == 'y':
        http_port = input('请输入项目端口:\n')
        pidfile_path = BASE_DIR / 'logs/master.pid'
        daemonize_path = BASE_DIR / 'logs/worker.log'
        pidfile_path.touch()
        daemonize_path.touch()

        with open(BASE_DIR / 'configs/uwsgi.ini', 'w') as file:
            file.write(f"""
[uwsgi]
chdir = {BASE_DIR}
module = project.wsgi:application
master = True
processes = 8
max-requests = 5000
harakiri = 60
http = :{http_port}
uid = root
gid = root
pidfile = {pidfile_path}
daemonize = {daemonize_path}
vacuum = True
""")


if __name__ == '__main__':
    run()
