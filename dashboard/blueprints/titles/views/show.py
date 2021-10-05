from flask import render_template
from flask.views import View
from dashboard.config import conf

from search.readers import ESReader


class ShowTitle(View):
    def dispatch_request(self, title_id):
        reader = ESReader(
            config=dict(
                host=conf.get("es", "host"),
                port=conf.getint("es", "port"),
                index=conf.get("es", "index_name"),
            )
        )
        titles, titles_total = reader.find_by_title_id(title_id=title_id)
        if titles_total["value"] > 1:
            raise Exception(f"More than one title under title id: {title_id}")
        return render_template(
            "titles/show.html",
            title=titles[0],
        )
