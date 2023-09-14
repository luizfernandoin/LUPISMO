from app import db


class Thoughts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(150), nullable=False)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)

    def __init__(self, author) -> None:
        self.author = author
    
    def __repr__(self):
        return f'Author %r>' % self.author
