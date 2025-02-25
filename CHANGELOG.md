# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [2025-02-24]

### Added
- **Dockerization of the application** 🐳
  - [Dockerfile] Initial Docker setup [Major]
  - [docker-compose.yml] Added Docker Compose configuration [Major]

- **User management feature** 👥
  - [api/serializers.py] Implemented user registration serialization [Minor]
  - [api/views.py] Added user registration endpoint [Minor]
  - [HydroponicsSystem/urls.py] Registered new user management API routes [Patch]

- **API Documentation** 📖
  - [HydroponicsSystem/settings.py] Integrated Swagger for API documentation [Minor]
  - [HydroponicsSystem/urls.py] Added Swagger routes [Patch]

### Changed
- [HydroponicsSystem/settings.py] Updated settings to support Docker [Patch]
- [requirements.txt] Updated dependencies for Docker support [Patch]
- [api/views.py] Updated docstrings and solved unordered `object_list` issue [Patch]

## [2025-02-23]

### Added
- **User authentication and authorization** 🔑
  - [HydroponicsSystem/urls.py] Added token authentication endpoints [Minor]
  - [HydroponicsSystem/settings.py] Integrated `rest_framework.authentication` [Minor]

## [2025-02-22]

### Added
- **Initial API structure** 🚀
  - [api/models.py] Created base models [Major]
  - [api/views.py] Implemented core API logic [Major]
  - [api/serializers.py] Created serializers for API endpoints [Major]
  - [api/urls.py] Registered API routes [Major]
  - [HydroponicsSystem/settings.py] Configured Swagger API documentation [Minor]

### Changed
- [HydroponicsSystem/urls.py] Registered `api.urls` in the main project [Patch]
- [api/views.py] Fixed issue with `.queryset` handling [Patch]

## [2025-02-21]

### Added
- **Project initialization** 🏗️
  - [HydroponicsSystem/settings.py] Initial Django settings setup [Major]
  - [HydroponicsSystem/urls.py] Initial URL routing [Major]
  - [HydroponicsSystem/wsgi.py] WSGI application setup [Major]
  - [.gitignore] Added default `.gitignore` for Django projects [Patch]
  - [README.md] Added project documentation [Patch]
