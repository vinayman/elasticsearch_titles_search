from flask.views import View
from flask import render_template


class ShowDashboard(View):
    def dispatch_request(self):
        return render_template(
            "dashboard/show.html",
        )
