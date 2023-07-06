from post.models import LikePostModel, PostModel


def is_user_has_likes(user_id: int, max_like: int) -> bool:
    if max_like > LikePostModel.objects.filter(user_id=user_id).count():
        return True
    return False


def is_user_has_posts(user_id: int, max_posts: int) -> bool:
    if max_posts > PostModel.objects.filter(author_id=user_id).count():
        return True
    return False
