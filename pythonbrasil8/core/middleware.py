# -*- coding: utf-8 -*-

from django.conf import settings


class CacheMiddleware(object):

    def process_response(self, request, response):
        if request.user.is_authenticated():
            response["Cache-Control"] = "no-cache"
            return response

        if not response.get("Cache-Control"):
            response["Cache-Control"] = "max-age=%d" % settings.PAGE_CACHE_MAXAGE

        if response.get("Vary") and "Cookie" in response["Vary"]:
            parts = response["Vary"].split(", ")
            parts.remove("Cookie")
            response["Vary"] = ", ".join(parts)

        return response
