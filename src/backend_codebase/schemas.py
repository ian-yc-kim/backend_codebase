from marshmallow import Schema, fields, validate

class UserInputSchema(Schema):
    id = fields.UUID(required=False, dump_only=True)
    user_id = fields.UUID(required=False, allow_none=True, missing=None)
    plot = fields.Str(required=True, validate=validate.Length(min=1))
    setting = fields.Str(required=True, validate=validate.Length(min=1))
    theme = fields.Str(required=True, validate=validate.Length(min=1))
    conflict = fields.Str(required=True, validate=validate.Length(min=1))
    additional_preferences = fields.Dict(required=False, allow_none=True, missing=None)
    ai_generated_content = fields.Str(required=False, dump_only=True)
    created_at = fields.DateTime(required=False, dump_only=True)
    updated_at = fields.DateTime(required=False, dump_only=True)

class FeedbackSchema(Schema):
    feedback = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(required=False, dump_only=True)
    updated_at = fields.DateTime(required=False, dump_only=True)
