from mongoengine import Document, StringField, ListField

class Movies(Document):
    name = StringField(required=True, unique=True)
    casts = ListField(StringField(), required=True)
    genres = ListField(StringField(), required=True)
