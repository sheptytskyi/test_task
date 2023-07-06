from dataclasses import dataclass
import yaml


@dataclass
class SocialNetworkConfigRules:
    number_of_users: int | None = None
    max_posts_per_user: int | None = None
    max_likes_per_user: int | None = None

    @classmethod
    def get_config(cls) -> 'SocialNetworkConfigRules':
        with open('bot/config.yaml', 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            return cls(**data)
