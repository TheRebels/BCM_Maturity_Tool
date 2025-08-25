from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)

	def __str__(self) -> str:
		return self.name


class User(AbstractUser):
	ROLE_ADMIN = 'admin'
	ROLE_COORDINATOR = 'coordinator'
	ROLE_CHAMPION = 'champion'
	ROLE_STEERING = 'steering'

	ROLE_CHOICES = [
		(ROLE_ADMIN, 'Admin'),
		(ROLE_COORDINATOR, 'BCM Coordinator'),
		(ROLE_CHAMPION, 'Business Unit Champion'),
		(ROLE_STEERING, 'Steering Committee'),
	]

	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CHAMPION)
	department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')


class Domain(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order', 'name']

	def __str__(self) -> str:
		return self.name


class Question(models.Model):
	ISO_SCALE_MIN = 0
	ISO_SCALE_MAX = 5

	domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='questions')
	text = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['domain__order', 'order', 'id']

	def __str__(self) -> str:
		return f"[{self.domain.name}] {self.text[:60]}"


class Assessment(models.Model):
	STATUS_DRAFT = 'draft'
	STATUS_SUBMITTED = 'submitted'
	STATUS_VALIDATED = 'validated'

	STATUS_CHOICES = [
		(STATUS_DRAFT, 'Draft'),
		(STATUS_SUBMITTED, 'Submitted'),
		(STATUS_VALIDATED, 'Validated'),
	]

	title = models.CharField(max_length=255)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='assessments')
	owner = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='owned_assessments')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
	deadline = models.DateField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	overdue_reschedule_count = models.PositiveIntegerField(default=0)

	def __str__(self) -> str:
		return f"{self.title} - {self.department.name}"


class Response(models.Model):
	assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='responses')
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
	rating = models.IntegerField(null=True, blank=True)
	comment = models.TextField(blank=True)
	created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='responses_created')
	updated_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='responses_updated')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('assessment', 'question')


class Evidence(models.Model):
	ALLOWED_TYPES = [
		('application/pdf', 'PDF'),
		('application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'DOCX'),
		('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'XLSX'),
	]

	response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='evidence')
	file = models.FileField(upload_to='evidence/%Y/%m/%d')
	content_type = models.CharField(max_length=150)
	version = models.PositiveIntegerField(default=1)
	uploaded_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='evidence_uploaded')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['response_id', 'version']


class AuditLog(models.Model):
	ACTION_LOGIN = 'login'
	ACTION_UPLOAD = 'upload'
	ACTION_SCORE_CHANGE = 'score_change'
	ACTION_SUBMIT = 'submit'
	ACTION_VALIDATE = 'validate'

	ACTION_CHOICES = [
		(ACTION_LOGIN, 'Login'),
		(ACTION_UPLOAD, 'Evidence Upload'),
		(ACTION_SCORE_CHANGE, 'Score Change'),
		(ACTION_SUBMIT, 'Assessment Submit'),
		(ACTION_VALIDATE, 'Assessment Validate'),
	]

	actor = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	action = models.CharField(max_length=50, choices=ACTION_CHOICES)
	context = models.CharField(max_length=255, blank=True)
	metadata = models.JSONField(default=dict, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']
