# Linux VPS on AWS Setup

For this demonstration, we are using an AWS t2.micro instance with Ubuntu Server. The entire project's configuration resides on a single server, including the database, static files, and source code. In larger projects, it's recommended to separate these components, with the database having its own server, a load balancer for the application, and serving media and static files from a Content Delivery Network (CDN). The installation method shown in this guide can be applied to any Linux server with Ubuntu Server, not just AWS. Any provider that offers access to a Linux machine will work.

## Creating the Server

To create the server, follow these steps:

1. Access the AWS Management Console.
2. Navigate to the Amazon EC2 section.
3. Click the "Launch Instance" button.
4. Choose "Ubuntu 16.04" as the desired Operating System.
5. Select the instance type that suits your needs (t2.micro is part of the free tier).
6. Specify the desired amount of storage (GB) for your instance.
7. Assign a descriptive name to the instance.
8. Create a new security group with ports 22, 80, and 8000 open from any IP address via TCP protocol.
9. Create new SSH keys and download them to your computer.

## Connecting to the Server

To connect to the server, use the SSH key you downloaded earlier. It's essential to keep this key safe, as losing it would mean losing access to the server.

1. Set the key file's permissions to read-only:

```bash
chmod 0400 PicScape.pem
```

2. Connect to the server using the public IP address assigned by AWS: 

```bash
sudo ssh -i PicScape.pem ubuntu@IP
```

Make sure to replace `PicScape.pem` with the actual name of your SSH key file and `IP` with the server's public IP address.

## Initial Server Configuration

### Updating Packages

As a good practice, update the operating system's packages when connecting to the server for the first time:

```bash
sudo apt-get update && sudo apt-get upgrade
```

### Creating a New User

Create a new user with a home directory with sudo privileges.

```bash
sudo useradd -g sudo -m picscape
```

Set a secure password for the new user:

```bash
sudo passwd picscape
```

Log in with the new user:

```bash
su picscape
```

Change the default shell to bash:

```bash
bash
```

Move to the `/srv/www` directory:

```bash
cd /srv
sudo mkdir www
sudo chmod 777 www
```

### Installing Dependencies

```bash
sudo apt-get install python3-pip python3-dev postgresql postgresql-contrib libpq-dev git nginx gunicorn
```

## Configure PostgreSQL

Log in as the PostgreSQL user:

```bash
sudo su postgres
```

Access the PostgreSQL interactive shell:

```bash
psql
```

Configure PostgreSQL by performing the following steps within the interactive shell:

1. Create a database:

```sql
CREATE DATABASE picscape;
```

2. Create a user for the database:

```sql
CREATE USER my_user WITH PASSWORD 'password';
```

3. Grant all privileges to the user for the database:

```sql
GRANT ALL PRIVILEGES ON DATABASE picscape TO my_user;
```

Exit the shell by typing `\q` followed by `exit` to leave the PostgreSQL session.

## Configure the Project

### Clone the Project

Clone the project from GitHub:

```bash
git clone https://github.com/jsurrea/PicScape.git picscape
```

### Set Up Virtual Environment

Install `virtualenv`:

```bash
sudo pip3 install virtualenv
```

Create a virtual environment:

```bash
virtualenv -p $(which python3) .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

### Install Dependencies

Install project dependencies, including those required for Pillow:

```bash
sudo apt-get install libjpeg-dev
```

Navigate to the project folder:

```bash
cd picscape
```

Install Python project dependencies:

```bash
pip install -r requirements.txt
```

### Set Environment Variables

Add some environment variables to the `~/.bashrc` file for local testing:

```bash
vim ~/.bashrc
```

Add variables similar to the following, replacing them with your actual values:

```bash
export PICSCAPE_SECRET_KEY="django-insecure-pcd#=y&javeopmt#)*5v7&y-w=d-czug3=$#u5yj#jef&rog_w"
export PICSCAPE_DB_NAME="picscape"
export PICSCAPE_DB_USER="my_user"
export PICSCAPE_DB_PASSWORD="password"
export PICSCAPE_DB_PORT="5432"
export PICSCAPE_DB_HOST="localhost"
export DJANGO_SETTINGS_MODULE="picscape.settings"
```

Save the file and escape vim with `ESC` key followed by `:wq`.

Reload the variables:

```bash
source ~/.bashrc
```

If your virtual environment gets deactivated, reload it:

```bash
cd ..
source .venv/bin/activate
cd picscape/
```

### Edit Production Settings

Edit the `ALLOWED_HOSTS` variable in the production settings file:

```bash
vim picscape/settings.py
```

Update the variable to include your domain or IP:

```python
ALLOWED_HOSTS = ['ec2-54-152-101-7.compute-1.amazonaws.com']
```

Set the Debug mode to False:

```python
DEBUG = False
```

Set the root for static files (you might need to delete the STATICFILES_DIRS if you decide to set them in the same location):

```python
STATIC_ROOT = BASE_DIR / "static"
# STATICFILES_DIRS = [BASE_DIR / "static"]
```

Save the file and escape vim with `ESC` key followed by `:wq`.

## Sanity Check

Perform the following checks to ensure the project is running correctly:

1. Reflect Django's model in PostgreSQL:

```bash
./manage.py makemigrations
./manage.py migrate
```

2. Create a superuser for administrative access:

```bash
./manage.py createsuperuser
```

3. Run the development server:

```bash
./manage.py runserver 0.0.0.0:8000
```

4. Run Gunicorn:

```bash
gunicorn picscape.wsgi -b 0.0.0.0:8000
```

If everything is configured correctly, steps 3 and 4 should display your site at the specified URL or IP on port 8000.

## Configure Nginx

1. Log in as the superuser:

```bash
sudo su -
```

2. Navigate to the Nginx directory:

```bash
cd /etc/nginx/
```

3. Remove the old configuration files:

```bash
rm sites-*/default
```

4. Create a new Nginx configuration file:

```bash
vim sites-available/app
```

Add the following configuration to the file, replacing `ec2-54-152-101-7.compute-1.amazonaws.com` with your domain and the `static` and `media` directories:

```nginx
upstream django_app {
    server 127.0.0.1:8000;
}

server {

    listen 80;
    server_name ec2-54-152-101-7.compute-1.amazonaws.com;

    access_log /var/log/nginx/app.log;
    error_log /var/log/nginx/app.error.log;

    location /static {
        autoindex on;
        alias /srv/www/picscape/static;
    }

    location /media {
        autoindex on;
        alias /srv/www/picscape/media;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        proxy_pass http://django_app;
    }

}
```

Save the file and escape vim with `ESC` key followed by `:wq`.

5. Create a symbolic link to enable the configuration:

```bash
ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
```

## Configuring Gunicorn

1. Exit Current Session

```bash
exit
```

2. Create the `deploy` and `logs` directories:

```bash
mkdir deploy logs
```

3. Create Gunicorn Start Script

```bash
vim deploy/gunicorn_start
```

Paste the following content into the file and save it:

```bash
#!/bin/bash

NAME="picscape"
VIRTUALENV="/srv/www/.venv/"
DJANGODIR="/srv/www/picscape/"
USER=picscape
GROUP=sudo
NUM_WORKERS=3
DJANGO_WSGI_MODULE=picscape.wsgi

echo "Starting $NAME as `whoami`"

cd $VIRTUALENV
source bin/activate
cd $DJANGODIR

export PICSCAPE_SECRET_KEY="django-insecure-pcd#=y&javeopmt#)*5v7&y-w=d-czug3=$#u5yj#jef&rog_w"
export PICSCAPE_DB_NAME="picscape"
export PICSCAPE_DB_USER="my_user"
export PICSCAPE_DB_PASSWORD="password"
export PICSCAPE_DB_PORT="5432"
export PICSCAPE_DB_HOST="localhost"

export DJANGO_SETTINGS_MODULE="picscape.settings"

export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec gunicorn ${DJANGO_WSGI_MODULE} \
        --workers $NUM_WORKERS \
        --user=$USER --group=$GROUP \
        --log-level=debug \
        --bind=127.0.0.1:8000
```

Save the file and escape vim with `ESC` key followed by `:wq`.

4. Make the Script Executable

```bash
chmod +x deploy/gunicorn_start
```

5. Test the Script

```bash
deploy/gunicorn_start
```

Ensure that Gunicorn starts without errors.

## Creating a Service

1. Switch to Superuser

```bash
sudo su -
```

2. Navigate to the Services Directory

```bash
cd /etc/init.d
```

3. Create a Service Script

```bash
vim picscape
```

Add the following content to the `picscape` file:

```bash
#!/bin/bash
### BEGIN INIT INFO
# Provides:          picscape
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start PicScape Service
# Description:       Start the PicScape service.
### END INIT INFO

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting PicScape Service"
    /srv/www/picscape/deploy/gunicorn_start
    ;;
  stop)
    echo "Stopping PicScape Service"
    # Add any stop commands here, if needed
    ;;
  restart)
    echo "Restarting PicScape Service"
    /srv/www/picscape/deploy/gunicorn_start
    ;;
  *)
    echo "Usage: /etc/init.d/picscape {start|stop|restart}"
    exit 1
    ;;
esac

exit 0
```

Save the file and escape vim with `ESC` key followed by `:wq`.

4. Make the Script Executable

```bash
sudo chmod +x /etc/init.d/picscape
```

5. Add the Service to Startup

```bash
sudo update-rc.d picscape defaults
```

6. Start the Service

```bash
sudo service picscape start
```

This will start your Django application with Gunicorn as a background service.

7. Collect Static Files

Return to `picscape` user:

```bash
exit
```

Now you should be located at `/srv/www/picscape`. Run the following Django utility:

```bash
./manage.py collectstatic
```

Your Django application should now be running as a service managed by Gunicorn, and Nginx should be serving the application at the specified IP address and port.
