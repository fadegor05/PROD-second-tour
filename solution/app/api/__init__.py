from .ping import ping_handler
from .countries import get_countries_by_region_handler, get_country_by_alpha2_handler
from .auth import register_user_handler
from .me import get_profile_handler, patch_profile_handler
from .profiles import get_profile_by_login_handler
from .friends import post_friend_add_handler, post_friend_remove_handler, get_friends_handler
from .posts import post_new_post_handler, get_post_by_uuid_handler