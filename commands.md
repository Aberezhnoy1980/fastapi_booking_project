## Run app

```SHELL
python3 main.py
```
<hr>

## Start DB

```SHELL
docker compose --project-directory ./database up
```

<hr>

## Initial migration

```SHELL
alembic revision --autogenerate -m "initial migration"
```

### Migration

```SHELL
alembic upgrade head
```