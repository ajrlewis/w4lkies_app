from urllib.parse import urlparse


def htmx_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        # HTMX request returning 302 likely is login required.
        # Take the redirect location and send it as the HX-Redirect header value,
        # with 'next' query param set to where the request originated. Also change
        # response status code to 204 (no content) so that htmx will obey the
        # HX-Redirect header value.
        if request.headers.get("HX-Request") == "true" and response.status_code == 302:
            ref_header = request.headers.get("Referer", "")
            if ref_header:
                referer = urlparse(ref_header)
                querystring = f"?next={referer.path}"
            else:
                querystring = ""

            redirect = urlparse(response["location"])
            response.status_code = 204
            response.headers["HX-Redirect"] = f"{redirect.path}{querystring}"
        return response

    return middleware
