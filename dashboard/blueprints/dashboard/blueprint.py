from flask import Blueprint

from .views import ShowDashboard

dashboard = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/dashboard/static",
)
dashboard.add_url_rule("/", methods=("GET",), view_func=ShowDashboard.as_view("show"))
