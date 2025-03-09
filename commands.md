## Run app

```SHELL
python3 src/main.py
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

`"initial migration"` - пользовательское имя миграции

### Migration

```SHELL
alembic upgrade head
```

### Rollback

```SHELL
alembic downgrade 7a3c7870706b
```

`7a3c7870706b` - номер предыдущей ревизии. Можно указать значение `-1`