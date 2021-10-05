from schematics.models import Model
from schematics.types import StringType, ListType, ModelType


class TitlePrefixes(Model):
    input = ListType(StringType())


class Title(Model):
    title_id = StringType()
    titles = ListType(StringType())
    titles_prefixes = ModelType(TitlePrefixes)
