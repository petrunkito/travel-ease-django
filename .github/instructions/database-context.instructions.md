---
applyTo: "**/*.{py,sql,md}"
description: "Use when working on models, serializers, migrations, or SQL to keep consistency with project database context"
---

# Database Context Instruction

Before creating or editing models, serializers, migrations, or booking/payment endpoints:
- Read `travel_ease.sql` as schema source of truth.
- Read `docs/database-context.md` as summarized domain context.

## Implementation rules
- Keep Django naming in English, map from SQL names explicitly.
- Do not change relationships without updating `docs/database-context.md`.
- If SQL and Django diverge, document the reason in `docs/database-context.md`.

## Validation checklist
1. Foreign keys preserved correctly.
2. Nullability and defaults reviewed.
3. Related endpoint serializers validate relationship integrity.
4. Tests cover core reservation and payment flows.
