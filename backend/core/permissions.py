from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')


class IsCoordinatorOrAdmin(BasePermission):
	def has_permission(self, request, view):
		if not (request.user and request.user.is_authenticated):
			return False
		return request.user.role in ('admin', 'coordinator')


class ReadOnly(BasePermission):
	def has_permission(self, request, view):
		return request.method in SAFE_METHODS


class DepartmentScopedQuerysetMixin:
	"""Filter queryset by user's department unless admin/coordinator."""
	def get_queryset(self):
		qs = super().get_queryset()
		user = self.request.user
		if not user.is_authenticated:
			return qs.none()
		if getattr(user, 'role', None) in ('admin', 'coordinator'):
			return qs
		# Champion/Steering: restrict assessments and related objects by department
		model = qs.model
		if model.__name__ == 'Assessment':
			return qs.filter(department=user.department)
		if model.__name__ == 'Response':
			return qs.filter(assessment__department=user.department)
		if model.__name__ == 'Evidence':
			return qs.filter(response__assessment__department=user.department)
		return qs