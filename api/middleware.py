from django.utils import timezone

from .models import User


class LastActivityTraceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user: User = request.user
        if user.is_authenticated:
            user.last_activity = timezone.now()
            user.save()
        return response
