from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from .models import AuditLog, Evidence, Response


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
	AuditLog.objects.create(actor=user, action=AuditLog.ACTION_LOGIN, context="login")


@receiver(post_save, sender=Evidence)
def log_evidence_upload(sender, instance: Evidence, created, **kwargs):
	if created:
		AuditLog.objects.create(
			actor=instance.uploaded_by,
			action=AuditLog.ACTION_UPLOAD,
			context=f"evidence:{instance.id}",
			metadata={"response_id": instance.response_id, "version": instance.version},
		)


@receiver(post_save, sender=Response)
def log_score_change(sender, instance: Response, created, **kwargs):
	# Log on create and update if rating present
	if instance.rating is not None:
		AuditLog.objects.create(
			actor=instance.updated_by or instance.created_by,
			action=AuditLog.ACTION_SCORE_CHANGE,
			context=f"response:{instance.id}",
			metadata={"rating": instance.rating},
		)