from django.contrib.auth import get_user_model

User = get_user_model()


def is_free_place_for_new_user(max_users: int) -> bool:
    if max_users > User.objects.all().count():
        return True
    return False
