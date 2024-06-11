# Introduction

Welcome to my REST API project! This project is designed to provide a robust and scalable API for managing various resources. The API is built with Python and leverages SQLAlchemy for ORM functionality. It is hosted on DigitalOcean's App Platform, ensuring reliable and scalable infrastructure. The database used is PostgreSQL, providing a powerful and flexible database management system. It can be ran locally if desired.

# Technologies:

    - Infrastructure: DigitalOcean App Platform
    - Database: PostgreSQL 16
    - ORM: SQLAlchemy 2.0.30
    - Framweork: Flask 3.0.3
    - Programming Language: Python 3.12
    - Python Libraries:
        - Flask-RESTful (for building REST APIs)
        - SQLAlchemy (for ORM)
        - psycopg2 (PostgreSQL adapter for Python)
        - Other dependencies listed in requirements.txt

# Local setup

To run the project locally, follow these steps:


Clone the repository:


    git clone https://github.com/Manhatai/rest_api
    cd rest_api-develop

Create and activate a virtual environment:

    python3 -m venv venv
    source venv/bin/activate

Install the required dependencies:

    pip install -r requirements.txt

Setup environment variables in a .env file:

    REST_API_DB_HOST=""
    REST_API_DB_PORT=""
    REST_API_DB_NAME=""
    REST_API_DB_LOGIN=""
    REST_API_DB_PASSWORD=""
    REST_API_SECRET_KEY=""
    REST_API_IS_DEBUG="true"
    REST_API_ENV_NAME="LOCAL"
    REST_API_LOCAL_TOKEN="" # This ones just for local testing purposes, put your generated web token here
 

# Setting up the database:
Ensure that PostgreSQL 16 is installed and running. Create a new database and update the your environment variables accordingly.

Run database migrations:

    flask db init
    flask db migrate -m "initial migration"
    flask db upgrade


# Running locally:

    python app.py



Open your http client (postman/insomnia) and navigate to http://localhost:5000/authorize/register


# How to Deploy

The deployment process is integrated with GitHub and DigitalOcean. Follow these steps to deploy your application:

1. Push your code to GitHub:

Ensure your latest code is committed and pushed to the main branch of your GitHub repository.

2. Connect GitHub repository to DigitalOcean:

In your DigitalOcean dashboard, navigate to the App Platform and create a new app. Select the GitHub repository and branch you want to deploy.

3. Automatic Build and Deployment:

DigitalOcean will automatically build and deploy your application whenever you push changes to the connected branch on GitHub.

4. Configure Environment Variables:

Set up the necessary environment variables, such as the database URL, in the DigitalOcean App Platform settings.

5. Manage your database:

Follow 'Setting up the database' section for deploying your database in the cloud system.
