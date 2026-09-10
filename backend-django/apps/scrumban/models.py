from django.db import models
from django.db.models import F, Q


class Workspace(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkspaceMember(models.Model):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"
        GUEST = "guest", "Guest"

    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="members"
    )
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.MEMBER)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["workspace", "user"], name="unique_workspace_member"
            ),
        )

    def __str__(self):
        return f"{self.user_id} @ {self.workspace_id} ({self.role})"


class Board(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="boards"
    )
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=10)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["workspace", "key"], name="unique_board_key_per_workspace"
            ),
        )

    def __str__(self):
        return f"{self.key} - {self.name}"


class Sprint(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="sprints")
    name = models.CharField(max_length=128)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PLANNED)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ("start_date",)
        constraints = (
            models.CheckConstraint(
                condition=Q(end_date__gte=F("start_date")),
                name="end_date_gte_start_date",
            ),
        )

    def __str__(self):
        return self.name


class Column(models.Model):
    class Type(models.TextChoices):
        BACKLOG = "backlog", "Backlog"
        ACTIVE = "active", "Active"
        DONE = "done", "Done"

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    name = models.CharField(max_length=64)
    position = models.IntegerField(default=0)
    column_type = models.CharField(max_length=8, choices=Type.choices, default=Type.ACTIVE)
    wip_limit = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ("position",)
        constraints = (
            models.UniqueConstraint(
                fields=["board", "name"], name="unique_column_name_per_board"
            ),
            models.UniqueConstraint(
                fields=["board", "position"], 
                name="unique_column_position_per_board",
                deferrable=models.Deferrable.DEFERRED,
            ),
        )

    def __str__(self):
        return f"{self.board_id} / {self.name}"


class Label(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="labels"
    )
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=7, default="#FFFFFF")

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["workspace", "name"], name="unique_label_name_per_workspace"
            ),
        )

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"
        URGENT = 4, "Urgent"

    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="tasks")
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subtasks",
    )
    assignee = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    labels = models.ManyToManyField(Label, related_name="tasks", blank=True)

    title = models.CharField(max_length=64)
    description = models.TextField(default="", blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LOW)
    story_points = models.PositiveSmallIntegerField(default=1)
    position = models.IntegerField(default=0)
    due_date = models.DateField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("position",)
        indexes = (
            models.Index(fields=["due_date"], name="idx_task_due_date"),
            models.Index(fields=["priority"], name="idx_task_priority"),
            models.Index(
                fields=["column", "position"], name="idx_task_column_position"
            ),
        )

    def __str__(self):
        return self.title


class TaskActivity(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="activities")
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities",
    )
    from_column = models.ForeignKey(
        Column,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="activities_from",
    )
    to_column = models.ForeignKey(
        Column, on_delete=models.CASCADE, related_name="activities_to"
    )
    moved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("moved_at",)
        verbose_name_plural = "task activities"

    def __str__(self):
        return f"Task {self.task_id}: {self.from_column_id} -> {self.to_column_id}"


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Comment {self.pk} on Task {self.task_id}"
