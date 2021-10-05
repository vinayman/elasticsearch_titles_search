import re

from wtforms import Form, StringField


class SearchForm(Form):
    title = StringField("Title")
    q = StringField("Quick search")

    def get_data_dict(self, page=None):
        data = dict(self.data)
        if page:
            data["page"] = page
        return data

    @property
    def quick_search_query(self):
        query = dict()
        if self.q.data:
            query["q"] = self.q.data
        return query

    @property
    def advanced_search_query(self):
        query = dict()
        if not self.validate():
            return query
        if self.title.data:
            query["_titles"] = self.title.data.strip()
        return query
