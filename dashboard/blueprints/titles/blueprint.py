from flask import Blueprint

from .views import ListTitles, ShowTitle, SuggestTitles


titles = Blueprint("titles", __name__, template_folder="templates")
titles.add_url_rule(
    "/",
    methods=("GET",),
    view_func=ListTitles.as_view("list"),
)
titles.add_url_rule(
    "/show/<title_id>",
    methods=("GET",),
    view_func=ShowTitle.as_view("show"),
)
titles.add_url_rule(
    "/suggest/",
    methods=("GET",),
    view_func=SuggestTitles.as_view("suggest"),
)
