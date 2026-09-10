# System Requirements & Domain Specification

This directory defines the functional requirements and behavioral specifications for the Scrumban Dual Stack system.

It serves as a **Living Domain Specification (Specification by Example)**:

- **[`docs/architecture/erd.md`](../docs/architecture/erd.md)** specifies the **static data model** (entities, fields, relations, database constraints).
- **[`conventions.md`](./conventions.md)** specifies the **response/authorization contract** shared by every operation (status codes, error shape, the 404-vs-403 rule, "Standard Read/Write" definitions).
- **[`permissions.md`](./permissions.md)** specifies the **canonical role matrix** (`ADMIN` / `MEMBER` / `GUEST`) that every epic's capability matrix references.
- **`epics/`** specifies the **dynamic domain behavior** (state transitions, business logic invariants, authorization gates, and validation) for each capability domain.

## Specification Structure

Each epic in `epics/` follows the same structure:

```plaintext
Epic (Domain Capability)
 └── User Story (Actor Intent & Value)
      ├── Domain Rules & Definitions (precise definitions the scenarios rely on)
      ├── Capability Matrix (CRUD & baseline operations, referencing permissions.md)
      ├── Flowchart(s) / State Diagram (visual logic & decision trees)
      └── Scenarios (Gherkin-formatted, concrete behavioral rules & invariants)
```

Not every epic needs every section, e.g. an epic with no ambiguous terminology skips "Domain Rules & Definitions" rather than padding it out.

## Scenario Identifiers & Test Traceability

Individual scenarios have **stable, persistent identifiers** formatted as `<EPIC_CODE>-<NUMBER>`:

| Prefix | Epic Domain | Reference Document |
| --- | --- | --- |
| `WS-*` | Workspace Management (incl. Labels) | [workspace_management.md](epics/workspace_management.md) |
| `BO-*` | Board Management | [board_management.md](epics/board_management.md) |
| `CC-*` | Column Configuration | [column_configuration.md](epics/column_configuration.md) |
| `TL-*` | Task Lifecycle & Movement | [task_lifecycle.md](epics/task_lifecycle.md) |
| `TO-*` | Task Organization & Hierarchy | [task_organization.md](epics/task_organization.md) |
| `TC-*` | Task Collaboration & Comments | [task_collaboration.md](epics/task_collaboration.md) |
| `SP-*` | Sprint Planning & Lifecycles | [sprint_planning.md](epics/sprint_planning.md) |

### Referencing in Automated Tests

Automated tests in backend test suites (`backend-django`, `backend-fastapi`) and frontend tests should reference scenario IDs directly in test method names and docstrings:

```python
class TestTaskLifecycle(APITestCase):
    def test_tl_05_move_into_column_at_wip_limit_rejected(self):
        """TL-05: Move into a column at its WIP limit is rejected with 400."""
        # ...
```

## Epics Catalog

### 1. [Workspace Management](epics/workspace_management.md) (`WS-*`)

Workspaces, tenant boundaries, user membership, role-based permissions, and workspace-scoped labels.

### 2. [Board Management](epics/board_management.md) (`BO-*`)

Board creation, workspace-unique keys, and cascading deletion.

### 3. [Column Configuration](epics/column_configuration.md) (`CC-*`)

Workflow column ordering, column types (`backlog`, `active`, `done`), and WIP limits.

### 4. [Task Lifecycle](epics/task_lifecycle.md) (`TL-*`)

Task creation, movement between columns, intra-column reordering, WIP limit enforcement, activity logging, and cascading delete.

### 5. [Task Organization](epics/task_organization.md) (`TO-*`)

Labels, assignee assignment, priorities, story points, and parent-subtask cycle prevention.

### 6. [Task Collaboration](epics/task_collaboration.md) (`TC-*`)

Comment threads on tasks and author/admin modification permissions.

### 7. [Sprint Planning](epics/sprint_planning.md) (`SP-*`)

Sprint lifecycle (`planned` → `active` → `completed`), single active-sprint constraint, and incomplete task roll-over.
