# Linux VPS on AWS Setup

For this demonstration, we are using an AWS t2.nano instance with Ubuntu Server. The entire project's configuration resides on a single server, including the database, static files, and source code. In larger projects, it's recommended to separate these components, with the database having its own server, a load balancer for the application, and serving media and static files from a Content Delivery Network (CDN). The installation method shown in this guide can be applied to any Linux server with Ubuntu Server, not just AWS. Any provider that offers access to a Linux machine will work.

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

Create a new user without a home directory with sudo privileges. Replace <username> with the desired username:

```bash
sudo useradd -g sudo -M <username>
```

Set a secure password for the new user:

```bash
sudo passwd <username>
```

Log in with the new user:

```bash
su <username>
```

### Installing Dependencies

```bash
sudo apt-get install python3-pip python3-dev postgresql postgresql-contrib libpq-dev git nginx
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
