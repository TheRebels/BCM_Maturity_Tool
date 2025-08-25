from django.contrib import admin
from .models import Department, User, Domain, Question, Assessment, Response, Evidence, AuditLog


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	list_display = ("name",)
	search_fields = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ("username", "email", "role", "department")
	list_filter = ("role", "department")
	search_fields = ("username", "email")


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
	list_display = ("name", "order")
	list_editable = ("order",)
	search_fields = ("name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ("domain", "order", "text")
	list_filter = ("domain",)
	search_fields = ("text",)


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
	list_display = ("title", "department", "status", "deadline", "created_at")
	list_filter = ("status", "department")
	search_fields = ("title",)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
	list_display = ("assessment", "question", "rating", "updated_at")
	list_filter = ("assessment", "question")
	search_fields = ("comment",)


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
	list_display = ("response", "version", "content_type", "uploaded_at", "uploaded_by")
	list_filter = ("content_type",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
	list_display = ("actor", "action", "created_at")
	list_filter = ("action",)
	search_fields = ("context",)
