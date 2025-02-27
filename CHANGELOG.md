# Changelog

All notable changes to this project will be documented in this file.

## [Release 1.2]

## [2025-02-26]

### Added
- **Feature: Retrieve latest measurements** 📊
  - [api/serializers.py] Updated to include `get_latest_measurements_feature` [Minor]
  - [api/views.py] Modified to support fetching the latest 10 measurements [Minor]
  - [api/tests/tests.py] Added test for `get_latest_measurements_feature` [Patch]

### Changed
- **Refactored dependency management** 🔄
  - [Dockerfile] Migrated from `pip` to `poetry` [Major]
  - [docker-compose.yml] Updated dependency management system [Major]
  - [poetry.lock] Added poetry lockfile [Major]
  - [pyproject.toml] Introduced poetry configuration file [Major]
  - [README.md] Updated installation instructions for poetry [Patch]

## [Release 1.1]

## [2025-02-25]

### Added
- **License Added** 📜
  - [LICENSE] Created project license file [Major]

## [Release 1.0]

## [2025-02-25]
- **Add admin tools** 🛠️
  - [api/admin.py] Add models to admin [Minor]
  - [requirements.txt] Add libraries to requirements [Minor]
  - [HydroponicsSystem/urls.py] Registered new user management API routes [Patch]
  - [HydroponicsSystem/settings.py] Integrated Dev Tools [Minor]

### Added
- **Improved Test Coverage** 🧪
  - [api/tests/tests.py] Added more tests to increase test coverage [Major]
  - [api/tests/tests.py] Included negative test cases [Minor]
  - [api/tests/__init__.py] Created unit tests module [Patch]

- **Refactored Code for Better Maintainability** 🔄
  - [api/views.py] Refactored view logic to improve clarity and maintainability [Minor]
  - [api/serializers.py] Cleaned up serializer logic [Patch]

- **Fixed Response Code Issues** 🛠️
  - [api/views.py] Fixed `404 Not Found` returning instead of `403 Forbidden` [Patch]
  - [api/views.py] Fixed `201 Created` returning instead of `400 Bad Request` in some cases [Patch]
  - [api/models.py] Adjusted validation logic to correctly raise errors [Patch]

- **Update readme** 📖
  - [README.md] Update readme [Major]
  - [CODEOWNERS] Create information about code owners [Major]

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

- **Update changelog** 📖
  - [CHANGELOG.md] Update changelog [Major] 


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
