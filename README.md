# Postgres devcontainer

A Python container and a Postgres container

## Functionality
1. mounts volume of the postgres data directory to the working directory
1. Creates user, password and db from config in docker-compose.yml
1. Starts Postgres

## psql client

Add to your local machine like mac to test connectivity

```sh
brew install libpq
```

if `psql` is not found, run

```sh
brew link --force libpq
```

### connect

```sh
psql -h localhost -p 5432 -U postgres -d postgres
```

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