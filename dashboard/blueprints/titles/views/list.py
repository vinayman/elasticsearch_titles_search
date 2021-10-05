from flask import render_template, request
from flask.views import View

from dashboard.blueprints.titles.forms import SearchForm
from dashboard.config import conf
from dashboard.helpers import get_pagination

from search.readers import ESReader


class ListTitles(View):
    def dispatch_request(self):
        page_size = conf.getint("ui", "pagination_per_page")
        page_number = int(request.args.get("page", 1))
        form = SearchForm(request.args)
        reader = ESReader(
            config=dict(
                host=conf.get("es", "host"),
                port=conf.getint("es", "port"),
                index=conf.get("es", "index_name"),
            )
        )
        if form.quick_search_query or form.advanced_search_query:
            if form.quick_search_query:
                titles, titles_total = reader.find_titles_by_title(form)
            else:
                titles, titles_total = reader.find_titles_by_title(form)
        else:
            titles, titles_total = reader.find_all(
                skip_results=page_number, max_results=page_size
            )
        return render_template(
            "titles/list.html",
            form=form,
            titles=titles,
            titles_total=titles_total["value"],
            pagination=get_pagination(page_size, page_number, titles_total["value"]),
        )
