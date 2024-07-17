# Project Name

Django rest framework API project utilizing viewsets to generate endpoints and docker compose to ensure it works anywhere.

The project consist of two models, User and Household, having a one to many relationship, and endpoints to interact with them.

The project also contains oauth endpoints and the possibility to add security to the viewset as a permission_class, but for simplicity it was commented.

## Table of Contents

- Installation
- Usage
- API Endpoints
- Testing
- Technologies

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/thriskel/user-households-api.git
    cd user-households-api
    ```

2. Start docker compose:
    ```bash
    docker compose up --build
    ```

## Usage

You can access this project endpoints through localhost using 8000 port once the docker containers are up and running.

This project has the following Swagger urls:
/docs
/redoc

You can also use the django browsable api through each endpoint.

It is important to fill the .env file once you clone the repo to allow the correct execution of the django and postgres container.

Since this is a practical example Im committing the file with valid data, but that should not be done in a real product.

## API Endpoints

- /users/ ['POST', 'GET']
- /users/<userId>/ ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
- /users/<userId>/households/ ['GET', 'POST', 'DELETE']
- /users/<userId>/households/<householdId>/ ['PUT', 'PATCH', 'DELETE']

## Testing

1. Run tests:
    ```bash
    docker compose run test
    ```

## Technologies

- Django
- Django REST framework
- Swagger UI
- PostgreSQL
- Docker
