# Postgres devcontainer

A Python container and a Postgres container

## Functionality
1. mounts volume of the postgres data directory to the working directory
1. Creates user, password and db from config in docker-compose.yml
1. Runs `init.sql` to create a database and table
1. Starts Postgres

## psql client

psql is added to the Python contactiner or add to your local machine like mac to test connectivity

### from the app container

```sh
docker exec -it postgres_devcontainer-app-1 /bin/sh
psql -h db -U postgres -d postgres
```

### local machine 

```sh
brew install libpq
```

if `psql` is not found, run

```sh
brew link --force libpq
```

### test connection

```sh
nc -zv localhost 5432
```

### connect

```sh
psql -h localhost -p 5432 -U postgres -d postgres
```

### commands

* list users `\du`
* list database `\l`
* contact to a database `\c <database>`
* list tables `\dt`
* list schemas `\d <table name>`

### add data

This insert statement could have been added to `init.sql` but here we demonstrate how to run with `psql` from the project directory in the Python container

```sh
psql -h localhost -p 5432 -U postgres -d mydatabase -f insert.sql
```

## Flask Web Application

This repository also includes a simple Flask web application (`app.py`) that provides a web interface to interact with the `mytable` data in the PostgreSQL database.

**Features:**

*   View all entries in the table.
*   Add new entries (Name, Email, Started On timestamp).
*   Edit existing entries.
*   Delete entries.

**Running the Application:**

1.  Ensure the Docker containers are running (`docker-compose up -d`).
2.  Make sure you are inside the development container's shell. If you used VS Code's "Reopen in Container" feature, you are likely already there. Otherwise, use:
    ```bash
    docker exec -it postgres_devcontainer-app-1 /bin/bash
    ```
3.  Install the Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the Flask development server:
    ```bash
    flask run --host=0.0.0.0 --port=5000
    ```
5.  Open your web browser and navigate to `http://localhost:5000`.

## Resources


[Python PostgreSQL devcontainer](https://github.com/devcontainers/templates/tree/main/src/postgres/.devcontainer)

[dev container spec](https://containers.dev/implementors/json_reference/)

## License

This project is licensed under the [MIT License](LICENSE)

## Contributing

### Disclaimer: Unmaintained and Untested Code

Please note that this program is not actively maintained or tested. While it may work as intended, it's possible that it will break or behave unexpectedly due to changes in dependencies, environments, or other factors.

Use this program at your own risk, and be aware that:
1. Bugs may not be fixed
1. Compatibility issues may arise
1. Security vulnerabilities may exist

If you encounter any issues or have concerns, feel free to open an issue or submit a pull request.
