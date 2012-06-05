# -*- coding: utf-8 -*-

from django.conf import settings


class CacheMiddleware(object):

    def process_response(self, request, response):
        if not response.get("Cache-Control"):
            response["Cache-Control"] = "max-age=%d" % settings.PAGE_CACHE_MAXAGE
        vary = response.get("Vary")
        if not vary:
            response["Vary"] = "Accept, Cookie"
        else:
            if "Accept" not in vary:
                response["Vary"] += ", Accept"
            if "Cookie" not in vary:
                response["Vary"] += ", Cookie"
        return response
