from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class UpdateUserLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        member: User = request.user
        if member.is_authenticated:
            member.last_activity = timezone.now()
            member.save()
        return response
