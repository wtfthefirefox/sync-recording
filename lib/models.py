from marshmallow import Schema, fields

class DownloadFile(Schema):
    name = fields.Str()
