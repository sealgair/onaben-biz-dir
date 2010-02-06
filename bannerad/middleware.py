"""
"""
from bannerad.models import BannerAd

def banner_context(request):
    """
    Add a random banner add to the context
    """
    context = {}
    try:
        context['banner'] = BannerAd.objects.get_random()
    except BannerAd.DoesNotExist:
        pass
    return context