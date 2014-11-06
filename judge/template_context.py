from collections import defaultdict
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.utils.functional import SimpleLazyObject
from .models import Profile, MiscConfig, NavigationBar


def get_profile(request):
    if request.user.is_authenticated():
        return Profile.objects.get_or_create(user=request.user)[0]
    return None


def user_profile(request):
    return {'profile': SimpleLazyObject(lambda: get_profile(request))}


def comet_location(request):
    return {'EVENT_DAEMON_LOCATION': settings.EVENT_DAEMON_GET,
            'EVENT_DAEMON_POLL_LOCATION': settings.EVENT_DAEMON_POLL}


def __tab(request, nav_bar):
    for item in nav_bar:
        if item.pattern.match(request.path):
            return item
    return None


def general_info(request):
    nav = cache.get('navbar')
    if nav is None:
        nav = list(NavigationBar.objects.values())
        cache.set('navbar', nav, 86400)
    path = request.get_full_path()
    return {
        'nav_tab': __tab(request, nav),
        'nav_bar': nav,
        'LOGIN_RETURN_PATH': '' if path.startswith('/accounts/') else path
    }


def site(request):
    return {'site': Site.objects.get_current()}


class MiscConfigDict(dict):
    def __missing__(self, key):
        try:
            value = MiscConfig.objects.get(key=key).value
        except MiscConfig.DoesNotExist:
            value = ''
        self[key] = value
        return value


def misc_config(request):
    return {'misc_config': MiscConfigDict()}


def contest(request):
    if request.user.is_authenticated():
        contest_profile = request.user.profile.contest
        in_contest = contest_profile.current is not None
        participation = contest_profile.current
    else:
        in_contest = False
        participation = None
    return {'IN_CONTEST': in_contest, 'CONTEST': participation}