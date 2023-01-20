from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(
        r'^admin/',
        admin.site.urls
    ),
    # url(
    #     r'^api-auth/',
    #     include('rest_framework.urls')
    # ),
    # url(
    #     r'^api/',
    #     include('rvme.api.urls')
    # ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
