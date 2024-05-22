from marshmallow import Schema, fields

class RecordVideo(Schema):
    room_id = fields.Str(required=True)
