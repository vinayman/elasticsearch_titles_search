from flask.views import View
from flask import jsonify, request, url_for, current_app as app

from search.readers import ESReader

from dashboard.config import conf
from dashboard.blueprints.titles.errors import BadRequest
from dashboard.blueprints.titles.forms import SuggestForm


class SuggestTitles(View):
    def dispatch_request(self):
        form = SuggestForm(request.args)
        if not form.validate():
            raise BadRequest("Invalid input", details=form.errors)
        reader = ESReader(
            config=dict(
                host=conf.get("es", "host"),
                port=conf.getint("es", "port"),
                index=conf.get("es", "index_name"),
            )
        )
        titles = reader.find_titles_by_prefix(
            prefix=form.q.data, max_results=form.max_results.data
        )
        results = self._transform_titles_into_select2_results(titles)
        return jsonify(dict(code=200, results=results, count=len(results)))

    def _transform_titles_into_select2_results(self, titles):
        results = []
        for title in titles:
            results.append(
                dict(
                    id=title.title_id,
                    text=title.titles[0],
                    url=url_for("titles.show", title_id=title.title_id),
                    work=title.to_native(),
                )
            )
        return results
