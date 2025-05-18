from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Worker, Position, TaskType, Task


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", )

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name", )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "deadline", "is_completed", "priority", "task_type")
    list_filter = ("is_completed", "priority", "task_type")
    search_fields = ("name", "description")
    ordering = ("-deadline", )
    date_hierarchy = "deadline"
    list_editable = ("is_completed", "priority")

@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )  # type: ignore
    list_filter = UserAdmin.list_filter + ("position", )  # type: ignore
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("position", )}),  # type: ignore
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("position",)}),
    )