from datetime import datetime, timezone
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, email={self.email})>'

    def __str__(self):
        return f'User: {self.username}'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=32)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Thought(db.Model):
    __tablename__ = "thoughts"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), index=True)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    author = db.relationship('User', backref='thoughts')
    likes_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Thought(id={self.id}, text={self.text[:20]}..., author_id={self.author_id})>'

    def __str__(self):
        return f'Thought: {self.text}'

    def increment_likes(self):
        self.likes_count += 1

    def decrement_likes(self):
        if self.likes_count > 0:
            self.likes_count -= 1

    def increment_shares(self):
        self.shares_count += 1

    def decrement_shares(self):
        if self.shares_count > 0:
            self.shares_count -= 1

class Like(db.Model):
    __tablename__ = "likes"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    thought_id = db.Column(db.Integer, db.ForeignKey('thoughts.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Like(id={self.id}, user_id={self.user_id}, thought_id={self.thought_id})>'

    def __str__(self):
        return f'Like by User ID: {self.user_id} on Thought ID: {self.thought_id}'

class Share(db.Model):
    __tablename__ = "shares"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    thought_id = db.Column(db.Integer, db.ForeignKey('thoughts.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Share(id={self.id}, user_id={self.user_id}, thought_id={self.thought_id})>'

    def __str__(self):
        return f'Share by User ID: {self.user_id} on Thought ID: {self.thought_id}'
