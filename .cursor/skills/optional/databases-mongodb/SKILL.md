---
name: databases-mongodb
description: Optional MongoDB skill (document DB, BSON, aggregation, Atlas). Activate when AGENTS.md §2 Database includes MongoDB. Portable core databases skill remains PostgreSQL-only.
license: MIT
---

# Databases — MongoDB (Optional)

Stack-gated MongoDB skill. Lives under `.cursor/skills/optional/databases-mongodb/`.
**Activate when:** `AGENTS.md §2 Database includes MongoDB`.

## When to Use

- Document-centric models (JSON/BSON)
- Flexible schemas and rapid prototyping
- Aggregation pipelines
- Atlas cloud clusters
- Index design for MongoDB workloads

## Quick Start

```bash
# Atlas: create cluster → connection string
mongosh "mongodb+srv://cluster.mongodb.net/mydb"
db.users.insertOne({ name: "Alice", age: 30 })
db.users.find({ age: { $gte: 18 } })
```

## References

- **[mongodb-crud.md](references/mongodb-crud.md)** — CRUD, query operators, atomic updates
- **[mongodb-aggregation.md](references/mongodb-aggregation.md)** — Pipeline stages and patterns
- **[mongodb-indexing.md](references/mongodb-indexing.md)** — Index types and performance
- **[mongodb-atlas.md](references/mongodb-atlas.md)** — Atlas setup, monitoring, search

## Best Practices

- Embed for 1-to-few; reference for 1-to-many / many-to-many
- Index frequently queried fields
- Prefer aggregation pipeline for complex transforms
- Enable auth + TLS in production
