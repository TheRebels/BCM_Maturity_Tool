from rest_framework import serializers
from .models import Department, Domain, Question, Assessment, Response, Evidence, User


class DepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Department
		fields = ["id", "name", "description"]


class DomainSerializer(serializers.ModelSerializer):
	class Meta:
		model = Domain
		fields = ["id", "name", "description", "order"]


class QuestionSerializer(serializers.ModelSerializer):
	domain = DomainSerializer(read_only=True)
	class Meta:
		model = Question
		fields = ["id", "domain", "text", "order"]


class ResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Response
		fields = ["id", "assessment", "question", "rating", "comment", "created_at", "updated_at"]
		read_only_fields = ["created_at", "updated_at"]


class EvidenceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Evidence
		fields = ["id", "response", "file", "content_type", "version", "uploaded_at"]
		read_only_fields = ["version", "uploaded_at"]


class AssessmentSerializer(serializers.ModelSerializer):
	department = DepartmentSerializer(read_only=True)
	overall_score = serializers.SerializerMethodField()
	domain_scores = serializers.SerializerMethodField()

	class Meta:
		model = Assessment
		fields = [
			"id", "title", "department", "owner", "status", "deadline",
			"created_at", "updated_at", "overall_score", "domain_scores",
		]
		read_only_fields = ["created_at", "updated_at"]

	def get_overall_score(self, obj: Assessment):
		responses = Response.objects.filter(assessment=obj, rating__isnull=False)
		values = [r.rating for r in responses]
		return round(sum(values) / len(values), 2) if values else None

	def get_domain_scores(self, obj: Assessment):
		from collections import defaultdict
		acc: dict[int, list[int]] = defaultdict(list)
		qs = Response.objects.filter(assessment=obj, rating__isnull=False).select_related('question__domain')
		for r in qs:
			acc[r.question.domain_id].append(r.rating)
		result = {}
		for domain_id, ratings in acc.items():
			avg = round(sum(ratings) / len(ratings), 2)
			result[str(domain_id)] = avg
		return result


class UserSerializer(serializers.ModelSerializer):
	department = DepartmentSerializer(read_only=True)
	class Meta:
		model = User
		fields = ["id", "username", "email", "role", "department"]