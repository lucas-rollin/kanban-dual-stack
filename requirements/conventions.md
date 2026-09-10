# Conventions

This document defines core rules that both backend implementations (`backend-django`, `backend-fastapi`) must follow identically.

## Operations & Responses

- **Standard Read:** Requires authentication (available to `GUEST+`). Returns `200 OK` (or `404 Not Found` if missing or outside the caller's workspace). Lists are workspace-scoped and use default ordering.
- **Standard Write:** Requires `MEMBER` or `ADMIN` roles. Returns `201 Created` (create), `200 OK` (update), or `204 No Content` (delete). Read-only fields in updates are **silently ignored**.
- **Error Shape:** Backends must normalize to DRF-style formatting:
  - *Validation:* `{"<field>": ["<message>", ...]}`
  - *Business Rules:* `{"detail": "<message>"}`

## Security & Identifiers

- **Authorization Codes:**
  - `401 Unauthorized`: Unauthenticated.
  - `404 Not Found`: Authenticated, but a **non-member** of the workspace (hides resource existence).
  - `403 Forbidden`: Workspace member, but lacking the required role.

- **Formats:** All timestamps are ISO-8601 UTC. All entity references use numeric primary keys (`id`), never slugs.
- **Scenario IDs:** Stable identifiers for test traceability. Future additions must use next-free numbers without renumbering existing ones.
