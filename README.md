# Hospital Appointment Management System API

This repository contains a REST API built using Flask for managing hospital appointments. It allows users to create new appointments and retrieve existing ones. The application is dockerized for portability and uses SQLite as the database.

---

## Features

- **Create Appointments**: Add new appointments to the system.
- **Retrieve Appointments**: Fetch existing appointments from the system.
- **API Documentation**: Swagger integration for API documentation.
- **Portability**: Dockerized for ease of deployment.

---

## Tech Stack

- **Backend Framework**: Python (Flask-RESTful)
- **Database**: SQLite (with SQLAlchemy ORM)
- **Documentation**: Swagger
- **Containerization**: Docker

---

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8 or later
- Docker
- Git

### Clone the Repository

```bash
git clone https://github.com/your-username/hospital-appointment-management.git
cd hospital-appointment-management
```

## Install Dependencies

### Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Usage Instructions
### Run Locally

Start the Application:

```bash
python app.py
```

**Access the API**: Open your browser or API testing tool (e.g., Postman) and go to http://127.0.0.1:5000.

**Swagger Documentation**: The Swagger documentation is available at:
```bash
http://127.0.0.1:5000/swagger
```

## Docker Instructions
Build the Docker Image
```bash
docker build -t hospital-appointment-api .
```
Run the Docker Container
```bash
docker run -d -p 5000:5000 hospital-appointment-api
```
### Access the Application

Visit http://127.0.0.1:5000 to use the API.

## API Documentation

Visit http://127.0.0.1:5000/apidocs/ to view API documentation

## PPT Link

Access the project presentation here: Hospital Appointment Management System PPT

Credits

    Developer: Tejas Tupke
    Framework: Flask-RESTful
    Database: SQLite
    Containerization: Docker

## Contributing

Contributions are welcome! Please follow these steps:

    Fork the repository.
    Create a new branch for your feature (git checkout -b feature-name).
    Commit your changes (git commit -m 'Add some feature').
    Push to the branch (git push origin feature-name).
    Create a Pull Request.
