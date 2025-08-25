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