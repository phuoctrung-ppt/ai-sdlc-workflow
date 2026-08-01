---
name: databases
description: Work with PostgreSQL (relational database, SQL queries, psql CLI, pgAdmin). Use when designing schemas, writing SQL, optimizing indexes, running migrations, configuring replication, backups, roles/permissions, or analyzing query performance. For MongoDB, activate optional skill databases-mongodb when AGENTS.md §2 Database includes MongoDB.
license: MIT
---

# Databases Skill (PostgreSQL)

Portable core database skill focused on PostgreSQL. MongoDB documentation lives under `.cursor/skills/optional/databases-mongodb/` and activates when `AGENTS.md §2 Database includes MongoDB`.

## When to Use This Skill

Use when:
- Designing relational schemas and data models
- Writing SQL (joins, CTEs, window functions)
- Optimizing indexes and query performance
- Implementing database migrations
- Configuring backups, roles, and replication
- Analyzing slow queries with EXPLAIN
- Administering PostgreSQL deployments

## When to Choose PostgreSQL

- Strong consistency: ACID transactions critical
- Complex relationships: many-to-many joins, referential integrity
- SQL ecosystem: reporting tools, BI systems
- Data integrity: strict schema validation, constraints
- Complex queries: window functions, CTEs, analytical workloads

**Best for:** Financial systems, e-commerce transactions, ERP, CRM, data warehousing, analytics

## Quick Start

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql

# Connect
psql -U postgres -d mydb

# Basic operations
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, age INT);
INSERT INTO users (name, age) VALUES ('Alice', 30);
SELECT * FROM users WHERE age >= 18;
UPDATE users SET age = 31 WHERE name = 'Alice';
DELETE FROM users WHERE name = 'Alice';
```

## Common Operations

### Create/Insert
```sql
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');
INSERT INTO users (name, email) VALUES ('Alice', NULL), ('Charlie', NULL);
```

### Read/Query
```sql
SELECT * FROM users WHERE age >= 18;
SELECT * FROM users WHERE email = 'bob@example.com' LIMIT 1;
```

### Update
```sql
UPDATE users SET age = 25 WHERE name = 'Bob';
UPDATE users SET status = 'active' WHERE status = 'pending';
```

### Delete
```sql
DELETE FROM users WHERE name = 'Bob';
DELETE FROM users WHERE status = 'deleted';
```

### Indexing
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status_created ON users(status, created_at DESC);
```

## Reference Navigation

- **[postgresql-queries.md](references/postgresql-queries.md)** — SELECT, JOINs, subqueries, CTEs, window functions
- **[postgresql-psql-cli.md](references/postgresql-psql-cli.md)** — psql commands, meta-commands, scripting
- **[postgresql-performance.md](references/postgresql-performance.md)** — EXPLAIN, query optimization, vacuum, indexes
- **[postgresql-administration.md](references/postgresql-administration.md)** — User management, backups, replication, maintenance

## Python Utilities

Database utility scripts in `scripts/`:
- **db_migrate.py** — Generate and apply migrations
- **db_backup.py** — Backup and restore PostgreSQL
- **db_performance_check.py** — Analyze slow queries and recommend indexes

```bash
python scripts/db_migrate.py --db postgres --generate "add_user_index"
python scripts/db_backup.py --db postgres --output /backups/
python scripts/db_performance_check.py --db postgres --threshold 100ms
```

## Best Practices

- Normalize schema to 3NF; denormalize only for measured performance needs
- Use foreign keys for referential integrity
- Index foreign keys and frequently filtered columns
- Use EXPLAIN ANALYZE to optimize queries
- Regular VACUUM and ANALYZE maintenance
- Connection pooling (pgBouncer) for web apps

## Resources

- PostgreSQL: https://www.postgresql.org/docs/
- PostgreSQL Tutorial: https://www.postgresqltutorial.com/
