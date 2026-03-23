1. To give the agent access, the safest setup is: create a dedicated read-only PostgreSQL user, connect through a controlled path, and let the agent inspect only metadata and stats.

For Cloud SQL PostgreSQL, the usual connection paths are:

- `Cloud SQL Auth Proxy`
- Cloud SQL language connectors
- direct `psql` over private/public IP if your network is already configured

A practical minimum setup is:

- create a database user like `agent_ro`
- grant `CONNECT` on the target database
- grant `USAGE` on the target schemas
- grant `SELECT` on tables, views, and catalog-visible objects you want exposed
- grant access to stats objects you allow, including `pg_stat_statements` if enabled

Typical SQL:

```sql
CREATE ROLE agent_ro LOGIN PASSWORD 'strong-password';

GRANT CONNECT ON DATABASE your_db TO agent_ro;
GRANT USAGE ON SCHEMA public TO agent_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO agent_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO agent_ro;
```

If you need multiple schemas, repeat the `GRANT USAGE` and `GRANT SELECT` for each one.

For Cloud SQL specifically, the main difference is that you usually connect through the Auth Proxy or a connector, and administrative capabilities are limited compared with self-managed PostgreSQL because Cloud SQL does not give you true superuser access. Google documents Cloud SQL connection options and IAM auth here:

- https://cloud.google.com/sql/docs/postgres/sql-proxy
- https://cloud.google.com/sql/docs/postgres/connect-connectors
- https://cloud.google.com/sql/docs/postgres/iam-authentication

2. If the agent cannot connect directly, export metadata and let it analyze files. That is often the better first pass for production.

You have two good export modes:

- `schema-only dump`
  Good for tables, columns, indexes, constraints, views, functions, procedures, triggers.

```bash
pg_dump --schema-only -h HOST -U USER -d DBNAME > schema_only.sql
```

- targeted catalog exports
  Good when you want structured CSV/JSON for analysis.

Examples with `psql`:

```bash
psql "host=HOST dbname=DBNAME user=USER sslmode=require" ^
  -c "\copy (
    SELECT table_schema, table_name, table_type
    FROM information_schema.tables
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY table_schema, table_name
  ) TO 'tables.csv' CSV HEADER"
```

```bash
psql "host=HOST dbname=DBNAME user=USER sslmode=require" ^
  -c "\copy (
    SELECT schemaname, tablename, indexname, indexdef
    FROM pg_indexes
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    ORDER BY schemaname, tablename, indexname
  ) TO 'indexes.csv' CSV HEADER"
```

If you want JSON instead:

```sql
SELECT json_agg(t)
FROM (
  SELECT table_schema, table_name, table_type
  FROM information_schema.tables
  WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
  ORDER BY table_schema, table_name
) t;
```

For full Cloud SQL exports, Google documents `pg_dump` / `pg_dumpall` here:

- https://cloud.google.com/sql/docs/postgres/import-export/import-export-dmp

3. Yes, Cloud SQL makes some difference, but not to the overall approach.

Main differences:

- connection/auth is different: proxy, connectors, IAM options are common
- permissions are different: Cloud SQL uses `cloudsqlsuperuser`, not true PostgreSQL superuser
- extension management is restricted to supported extensions
- some server-level knobs are managed through Cloud SQL flags, not raw server config

For your use case, that means:

- structure mapping still works
- workload mapping still works if `pg_stat_statements` is available
- some admin-only inspection patterns may be unavailable
- extension enablement depends on Cloud SQL support and privileges

Cloud SQL does support `pg_stat_statements`:

- https://cloud.google.com/sql/docs/postgres/extensions

4. To check whether `pg_stat_statements` is enabled, use these checks in order.

Check whether the library is preloaded:

```sql
SHOW shared_preload_libraries;
```

If the result contains `pg_stat_statements`, that is the first requirement.

Check whether the extension is installed in the current database:

```sql
SELECT extname
FROM pg_extension
WHERE extname = 'pg_stat_statements';
```

Check whether the view is actually queryable:

```sql
SELECT count(*) FROM pg_stat_statements;
```

If you get rows back, it is working in that database.

A compact diagnostic query:

```sql
SELECT
  current_setting('shared_preload_libraries', true) AS shared_preload_libraries,
  EXISTS (
    SELECT 1 FROM pg_extension WHERE extname = 'pg_stat_statements'
  ) AS extension_installed;
```

Background from PostgreSQL docs:

- `pg_stat_statements` must be in `shared_preload_libraries`
- the extension must also be created in the database with `CREATE EXTENSION pg_stat_statements`

Source:

- https://www.postgresql.org/docs/current/pgstatstatements.html

5. Since Mermaid is fine, your current prompt output format is already aligned. No change needed there.

My recommendation is:

- first try direct read-only access if this is a non-production clone or a tightly controlled prod read path
- otherwise export `schema_only.sql` plus CSVs for tables, columns, indexes, FKs, routines, views, and `pg_stat_statements` output
- feed those files to the agent instead of the live database

If you want, I can do the next step and create:

- a Cloud SQL-specific setup checklist
- a ready-to-run metadata export script for Windows PowerShell
- a revised version of your enriched prompt tailored for Cloud SQL and file-based analysis only
