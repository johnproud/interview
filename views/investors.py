from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy import func

from app import db
from models.investors import Investor
from schemas.investors import filter_schema


class InvestorResources(Resource):
    def get(self):  # noqa
        errors = filter_schema.validate(request.args)
        if errors:
            return make_response(jsonify(errors), 400)

        filters = filter_schema.load(request.args)

        queryset = db.session.query(
            Investor.title, func.sum(Investor.total).label('sum_total')
        ).group_by(Investor.title).filter(
            Investor.week_start >= filters['week_start'],
            Investor.week_end <= filters['week_end'],
        )

        investors = {investor.title: investor.sum_total for investor in queryset}
        return dict(**investors, **request.args)
