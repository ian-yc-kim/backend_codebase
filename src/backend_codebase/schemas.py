from marshmallow import Schema, fields, validate

class UserInputSchema(Schema):
    user_id = fields.UUID(required=False)
    plot = fields.Str(required=True, validate=validate.Length(min=1))
    setting = fields.Str(required=True, validate=validate.Length(min=1))
    theme = fields.Str(required=True, validate=validate.Length(min=1))
    conflict = fields.Str(required=True, validate=validate.Length(min=1))
    additional_preferences = fields.Str(required=False)

class FeedbackSchema(Schema):
    input_id = fields.Int(required=True)
    feedback = fields.Str(required=True, validate=validate.Length(min=1))
