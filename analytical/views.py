from django.views.generic import RedirectView
from analytical.models import AnalyticMedia
from django.shortcuts import get_object_or_404
from analytical.utils import ViewCountWithRule


class AnalyticalMediaRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        analytic_media = get_object_or_404(AnalyticMedia, slug=kwargs.get('slug', None))
        setattr(self.request, 'data', {})
        ViewCountWithRule(analytic_media, self.request)()
        return analytic_media.media_source

