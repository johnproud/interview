from database import db


class Investor(db.Model):
    __tablename__ = 'investors'  # noqa

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    week_end = db.Column(db.Date, nullable=False)
