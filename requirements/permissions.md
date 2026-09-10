# Permissions

Every permission in this system is **workspace-scoped**, not accounting authentication which is always required.

## Roles

| Role | Summary |
| --- | --- |
| `ADMIN` | Full control: workspace settings, membership management, and the destructive/administrative operations, plus everything a `MEMBER` can do. |
| `MEMBER` | The default collaborator role: create/update/move/delete boards, columns, labels, tasks, sprints; comment. |
| `GUEST` | Read-only. Can view everything a `MEMBER` can but cannot create, update, delete, move, or comment on anything. |

## Capability Matrixe

Letters are positional, `C`reate, `R`ead, `U`pdate, `D`elete, with `-` marking a denied operation.

| Resource | Admin | Member | Guest | Notes / Conditions |
| :--- | :---: | :---: | :---: | :--- |
| **Workspace** | `CRUD` | `R---` | `R---` | Settings updates & deletion are Admin-only. |
| **Membership** | `CRUD` | `R---` | `R---` | Add / change role / remove restricted to Admin; see sole-Admin protection below. |
| **Board** | `CRUD` | `CRU-` | `R---` | Deletion is Admin-only. |
| **Column** | `CRUD` | `CRU-` | `R---` | Deletion is Admin-only, and additionally blocked while the column has tasks (see `CC-03`). |
| **Label** | `CRUD` | `CRUD` | `R---` | No Admin-only gate, any Member can manage labels. |
| **Task** | `CRUD` | `CRUD` | `R---` | No Admin-only gate; "move" is a variant of Update. |
| **Activity** | `R---` | `R---` | `R---` | System-generated only. It's a side effect of Task moves (see `TL-01`–`TL-03`). |
| **Comment** | `CR**` | `CR**` | `R---` | `*` Update is Author-only, regardless of role. Admin may additionally delete any comment. a Member may only delete their own. |
| **Sprint** | `CRUD` | `CRUD` | `R---` | No Admin-only gate; deletion additionally requires `status="planned"` (see `SP-06`). |

Two rows don't reduce to a simple role lookup and are governed by dedicated invariants documented in their own epics rather than this table:

- **Sole-Admin protection** — an `ADMIN` cannot demote or remove themselves (or be demoted/removed by another admin) if they are the workspace's last remaining `ADMIN`. See [workspace_management.md](./epics/workspace_management.md), `WS-03`.
- **Comment authorship** — editing is author-only regardless of role; an `ADMIN` can delete another member's comment but cannot edit it. See [task_collaboration.md](./epics/task_collaboration.md), `TC-02`/`TC-03`.

## Non-Members

A user with no `WorkspaceMember` record for a given workspace has no access to any resource within it, at any role level.
