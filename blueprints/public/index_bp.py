from datetime import datetime, timedelta
from flask import current_app, Blueprint, render_template, Response

index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/", methods=["GET"])
def get():
    return render_template("public/index.html"), 200


@index_bp.route("/sitemap.xml")
def sitemap():
    pages = []
    lastmod = datetime.now() - timedelta(days=10)
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods:
            exclude_urls = ["/admin/", "/static"]
            url = rule.rule
            page = {"url": url, "lastmod": lastmod.strftime("%Y-%m-%d")}
            if not any(exclude_url in url for exclude_url in exclude_urls):
                pages.append(page)
    sitemap_xml = render_template("public/sitemap.xml", pages=pages)
    return Response(sitemap_xml, mimetype="text/xml")
