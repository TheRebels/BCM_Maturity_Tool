from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Department


class Command(BaseCommand):
	help = "Seed default roles and an example admin if none exists"

	def handle(self, *args, **options):
		User = get_user_model()
		Department.objects.get_or_create(name="Corporate")
		if not User.objects.filter(is_superuser=True).exists():
			user = User.objects.create_superuser(
				username="admin",
				email="admin@example.com",
				password="admin123",
			)
			self.stdout.write(self.style.SUCCESS(f"Created superuser {user.username}"))
		else:
			self.stdout.write("Superuser already exists; skipping")