# -*- coding: utf-8 -*-


class CacheMiddleware(object):

    def process_response(self, request, response):
        if not response.get("Cache-Control"):
            response["Cache-Control"] = "max-age=300"
        vary = response.get("Vary")
        if not vary:
            response["Vary"] = "Accept, Cookie"
        else:
            if "Accept" not in vary:
                response["Vary"] += ", Accept"
            if "Cookie" not in vary:
                response["Vary"] += ", Cookie"
        return response
