# Bulk Certificate Generator API

## Overview

This project is a backend API for generating certificates in bulk.

The API accepts a list of recipients and certificate information, generates a certificate for each recipient using a predefined template, and tracks the status of each certificate.

## Technologies Used

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- ReportLab
- Pytest

## Features

- Bulk certificate generation
- Input validation
- PDF certificate generation
- Job status tracking
- Successful and failed certificate tracking
- Certificate retrieval
- Individual certificate failure handling
- Automated tests
- Swagger API documentation

## Project Structure

```text
Bulk Certificate Generator API
│
├── app
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── certificate.py
│   └── routes.py
│
├── certificates
├── tests
│   └── test_api.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── certificates.db