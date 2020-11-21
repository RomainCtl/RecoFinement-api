# RecoFinement - API service

![Test&Deploy badge](https://github.com/RomainCtl/Recofinement-api/workflows/Test%20and%20Deploy/badge.svg) ![Tests](https://github.com/RomainCtl/RecoFinement-api/blob/gh-pages/tests.svg) ![Coverage score](https://github.com/RomainCtl/RecoFinement-api/blob/gh-pages/coverage.svg)

* Tests results: [https://romainctl.github.io/RecoFinement-api/](https://romainctl.github.io/RecoFinement-api/)
* Documentation: [https://RomainCtl.github.io/RecoFinement/](https://RomainCtl.github.io/RecoFinement/)
* Master project repo: [https://github.com/RomainCtl/RecoFinement](https://github.com/RomainCtl/RecoFinement)

> Check instruction about requirements in the `README.md` file of the master project.

## Requirements

* [PostgreSQL](https://www.postgresql.org/) Server with a database with the name of your choice (Do not forget to define env variables, see next point).


## Configuration

In order to run correctly, the project needs to recover its configuration. To do so, just copy the `.env.default` file:

```bash
cp .env.default .env
```

Then replace the values, and in particular the variables for the connection to the database.


## Usage

Basic usage:
```bash
# Initialize project (install dependencies)
make init

# Update database to the last migration (or initialize it if it does not exist)
make db-updade

# Serve locally the development build
make serve

# Run all unit tests
make test
```

Display Makefile help (display all available targets):
```bash
make
# or
make help
```


## Database versionning

During the successive phases of development, you will have to modify the database (new table, new column, ...). In order to ensure that the database is up to date at each installation, a versioning procedure of the database has been set up with the [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) tool.

> All files and scripts produced by [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) are stored in the directory `./migrations/`.

To change the database structure and create a new database migration script, follow these steps:
1. Edit the [SQLAlchemy](https://www.sqlalchemy.org/) data models in the directory `./src/model/`
2. Run the following command to generate a new database migration script:
```bash
make db-migration version="explicit_version_name"
```
3. Check the contents of the generated script in the directory `./migrations/versions/<genrated-file>`. Sometimes [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) does not detect certain changes. In this case, you will have to do it manually

## Contribution

Contributions are managed using github's Pull Request (PR). After cloning the `master` branch of the project, use the following commands to create a new branch with its associated `Pull Request`:

```bash
# Create a feature branch and its PR
make git-branch feat="Adds a nice feature"

# Create a bug fix branch and its PR
make git-branch fix="Fix a bug"

# Create a documentation|support branch and its PR
make git-branch doc="Adds a nice documentation or support"
```
