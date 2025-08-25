from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Assessment, User


def notify_due_assessments():
	"""Send reminder emails for assessments due within 3 days."""
	now = timezone.now().date()
	upcoming = Assessment.objects.filter(deadline__isnull=False, deadline__gte=now, deadline__lte=now + timezone.timedelta(days=3))
	for a in upcoming.select_related('owner', 'department'):
		if a.owner and a.owner.email:
			send_mail(
				subject=f"Assessment due soon: {a.title}",
				message=f"Your assessment '{a.title}' for {a.department.name} is due on {a.deadline}.",
				from_email=settings.DEFAULT_FROM_EMAIL,
				recipient_list=[a.owner.email],
			)


def notify_overdue_assessments():
	"""Send reminders for overdue assessments."""
	today = timezone.now().date()
	overdue = Assessment.objects.filter(deadline__lt=today).exclude(status=Assessment.STATUS_VALIDATED)
	for a in overdue.select_related('owner', 'department'):
		if a.owner and a.owner.email:
			send_mail(
				subject=f"Assessment overdue: {a.title}",
				message=f"Assessment '{a.title}' for {a.department.name} is overdue since {a.deadline}.",
				from_email=settings.DEFAULT_FROM_EMAIL,
				recipient_list=[a.owner.email],
			)