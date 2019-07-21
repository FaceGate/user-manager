from marshmallow import Schema, fields


class CreateUserSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    profile_pictures = fields.List(fields.Url, required=True)
    group_ids = fields.List(fields.Int, required=True)
    expiration_date = fields.Date(required=True)
