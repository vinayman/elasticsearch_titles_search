import ast

from search.models import Title


class ESTransformer:
    def encode(self, raw_titles: dict) -> Title:
        if "titles" not in raw_titles or "title_id" not in raw_titles:
            raise KeyError(f"Original Title not present! raw_titles: {raw_titles}")
        titles = raw_titles["titles"]
        if isinstance(titles, str):
            titles = ast.literal_eval(raw_titles["titles"])
        return Title(
            dict(
                title_id=raw_titles["title_id"],
                titles=titles,
                titles_prefixes=dict(
                    input=self._generate_titles_prefixes(titles),
                ),
            )
        )

    def _generate_titles_prefixes(self, titles: list[str]) -> list[str]:
        prefixes = []
        for title in titles:
            prefixes.extend(self._generate_title_prefixes(title))
        return prefixes

    def _generate_title_prefixes(self, title: str) -> list[str]:
        tokens = title.split()
        return [" ".join(tokens[start:]) for start in range(len(tokens))]
