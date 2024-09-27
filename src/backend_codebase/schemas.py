from marshmallow import Schema, fields, validate

class UserInputSchema(Schema):
    """
    Schema for user input data.

    This schema is used to validate and serialize/deserialize user input data for the backend system.

    Fields:
    - id (UUID): Unique identifier for the user input. This field is read-only.
    - user_id (UUID): Unique identifier for the user. This field is optional and can be None.
    - plot (str): Plot description provided by the user. This field is required and must have at least 1 character.
    - setting (str): Setting description provided by the user. This field is required and must have at least 1 character.
    - theme (str): Theme description provided by the user. This field is required and must have at least 1 character.
    - conflict (str): Conflict description provided by the user. This field is required and must have at least 1 character.
    - additional_preferences (dict): Additional preferences provided by the user. This field is optional and can be None.
    - ai_generated_content (str): AI-generated content based on the user input. This field is read-only.
    - created_at (datetime): Timestamp when the user input was created. This field is read-only.
    - updated_at (datetime): Timestamp when the user input was last updated. This field is read-only.
    """
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
    """
    Schema for feedback data.

    This schema is used to validate and serialize/deserialize feedback data for the backend system.

    Fields:
    - feedback (str): Feedback provided by the user. This field is required and must have at least 1 character.
    - created_at (datetime): Timestamp when the feedback was created. This field is read-only.
    - updated_at (datetime): Timestamp when the feedback was last updated. This field is read-only.
    """
    feedback = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(required=False, dump_only=True)
    updated_at = fields.DateTime(required=False, dump_only=True)

class UserSchema(Schema):
    """
    Schema for user data.

    This schema is used to validate and serialize/deserialize user data for the backend system.

    Fields:
    - id (UUID): Unique identifier for the user. This field is read-only.
    - username (str): Username of the user. This field is required and must have at least 1 character.
    - email (str): Email address of the user. This field is required and must be a valid email address.
    - password (str): Password of the user. This field is required and must have at least 8 characters.
    - created_at (datetime): Timestamp when the user was created. This field is read-only.
    - updated_at (datetime): Timestamp when the user was last updated. This field is read-only.
    """
    id = fields.UUID(required=False, dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    created_at = fields.DateTime(required=False, dump_only=True)
    updated_at = fields.DateTime(required=False, dump_only=True)
