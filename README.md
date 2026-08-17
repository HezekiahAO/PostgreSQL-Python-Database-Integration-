# Week 3 — PostgreSQL & Python Database Integration

A small Python application (movies dataset) demonstrating PostgreSQL +
Python integration: schema design, parameterised queries, transaction
handling, logging, integration tests, and indexing.

## 1. Setup

```bash
# create the database
createdb week3_movies

# load schema + sample data
psql -d week3_movies -f schema.sql

# install Python dependencies
pip install -r requirements.txt
```

Set your DB credentials as environment variables (or edit the defaults in
`db_config.py`):

```bash
export DB_NAME=week3_movies
export DB_USER=postgres
export DB_PASSWORD=yourpassword
export DB_HOST=localhost
export DB_PORT=5432
```

## 2. Run the demo

```bash
python app.py
```

This will:
- insert a movie
- retrieve movies by genre
- run `EXPLAIN ANALYZE` on a genre lookup **before** an index exists
- create an index on `genre`
- run `EXPLAIN ANALYZE` again **after** the index exists (compare the plans —
  look for `Seq Scan` before vs `Index Scan`/`Bitmap Index Scan` after)
- demonstrate a rollback when an invalid rating is inserted

All operations are logged to `db_operations.log` and printed to console.

## 3. Run the tests

```bash
pytest -v
```

## 4. What each task requirement maps to

| Requirement | Where |
|---|---|
| Create DB + schema/tables | `schema.sql` |
| Import sample data | `schema.sql` (INSERT statements) |
| Connect Postgres to Python | `db_config.py`, `get_connection()` in `app.py` |
| Insert/retrieve records | `insert_movie()`, `get_movies_by_genre()` in `app.py` |
| Parameterised queries | every query uses `%s` placeholders, never string formatting |
| Transaction handling (COMMIT/ROLLBACK) | `with conn:` blocks + explicit `conn.rollback()` in `except` clauses |
| Logging | `logging` config at top of `app.py`, writes to `db_operations.log` |
| Integration tests | `test_integration.py` |
| Index + EXPLAIN/EXPLAIN ANALYZE | `create_genre_index()` + `explain_query_on_genre()` in `app.py` |

## 5. Notes on the index demo

Before the index, Postgres has to scan every row (`Seq Scan on movies`) to
find matching genres. After running `CREATE INDEX idx_movies_genre ON
movies (genre)`, Postgres can use the index instead. With only 20 rows the
planner *might* still choose a sequential scan (it's faster for tiny
tables) — if that happens, mention it in your write-up as an example of the
query planner making a cost-based decision, which is itself worth
discussing.

Personal NOTES:
A parameterised query is a secure way to write database queries by keeping your SQL code separate from user input.