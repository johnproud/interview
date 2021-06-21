from marshmallow import Schema, fields


class FilterInvestorsSchema(Schema):
    week_start = fields.Date(required=True, format="%Y-%m-%d")
    week_end = fields.Date(required=True, format="%Y-%m-%d")


filter_schema = FilterInvestorsSchema()
