# PicScape

PicScape is a social media platform built with Django that allows users to share and discover photos. It provides a user-friendly interface for uploading, liking, and commenting on photos, as well as following other users to stay updated with their posts. It can be easily deployed on your local machine to create your own private picture network!

## Table of Contents

- [About](#about)
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## About

PicScape is a project designed to showcase the power of Django in building a modern web application. It focuses on the following key aspects:

- **User Authentication**: Secure user registration and login.
- **User Profiles**: Customizable user profiles with profile pictures and biographies.
- **Photo Sharing**: Easy photo uploading, liking, and commenting.
- **Social Interaction**: Following other users to create a personalized feed.

## Features

- User registration and authentication.
- User profiles with profile pictures, biographies, and post counts.
- Photo uploading with automatic resizing and storage.
- Liking and commenting (coming soon!) on photos.
- User-to-user following for a personalized feed.
- Responsive design for a seamless user experience on different devices.

## Demo

You can see a live demo of PicScape at [https://ec2-54-152-101-7.compute-1.amazonaws.com](https://ec2-54-152-101-7.compute-1.amazonaws.com).

This project also comes configured with a preloaded SQLite database and media files. You can try a full demo with artificial data by installing the app without changing the database settings.

## Installation

Follow these steps to set up PicScape on your machine:

### VM configuration

Follow the deployment installation guide [here](deployment.md) for complete instructions on setting up the proyect on a Linux VPS with a cloud provider. Learn how to configure a PostgreSQL database, a NGINX web server and to run the Django project with Gunicorn.

### Prerequisites

Before you start, make sure you have the following prerequisites installed:

- Python 3.7+
- Django 4.2+
- PostgreSQL (or any other database of your choice)

### Clone the Repository

```bash
git clone https://github.com/jsurrea/PicScape
```

### Create a Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On macOS and Linux
venv\Scripts\activate     # On Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Database

Create a PostgreSQL database and update the database settings in `picscape/settings.py`.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-database',
        'USER': 'your-db-user',
        'PASSWORD': 'your-db-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Remember to delete the preloaded SQLite database `db.sqlite3` and the media image contents saved at `media/posts/photos` and `media/users/pictures`.

### Apply Migrations

```bash
python manage.py migrate
```

### Create a Superuser (access to admin site)

```bash
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

PicScape should now be running locally at `http://localhost:8000/`.

## Usage

- Access the admin panel at `http://localhost:8000/admin/`` to manage users, photos, and other data.
- Sign up for a new user account and start exploring the photo-sharing features.
- Customize your user profile by adding a profile picture and biography.
- Follow other users to see their posts in your personalized feed.
- Upload photos, like them, and leave comments to interact with the PicScape community.

## Contributing
We welcome contributions to make PicScape even better! If you'd like to contribute, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and test thoroughly.
3. Create a pull request with a clear description of your changes and why they are necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
