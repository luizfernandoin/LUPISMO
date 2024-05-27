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
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def joined_in(self):
        return self.created_at.strftime("%b %Y")
    
    def len_posted(self):
        return Thought.query.filter_by(author_id=self.id).count()
    

class Thought(db.Model):
    __tablename__ = "thoughts"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    author = db.relationship('User', backref='thoughts')
    likes_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Thought(id={self.id}, text={self.text[:20]}..., author_id={self.author_id}, likes_count={self.likes_count}, shares_count={self.shares_count})>'

    def __str__(self):
        return f'Thought: {self.text}'

    def increment_likes(self):
        self.likes_count += 1
        db.session.commit()

    def decrement_likes(self):
        if self.likes_count > 0:
            self.likes_count -= 1
        db.session.commit()

    def increment_shares(self):
        self.shares_count += 1
        db.session.commit()

    def decrement_shares(self):
        if self.shares_count > 0:
            self.shares_count -= 1
        db.session.commit()
            
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author': self.author,
            'likes': self.likes_count,
            'shares': self.shares_count
        }
    
    def user_liked(self, user_id):
        return Like.query.filter_by(user_id=user_id, thought_id=self.id).first() is not None
    
    def time_since_posted(self):
        now = datetime.now().replace(tzinfo=None)
        diff = now - self.created_at
        
        days = diff.days
        seconds = diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if days > 0:
            return f"{days} day(s) ago" if days > 1 else "a day ago"
        elif hours > 0:
            return f"{hours} hour(s) ago" if hours > 1 else "an hour ago"
        elif minutes > 0:
            return f"{minutes} minute(s) ago" if minutes > 1 else "a minute ago"
        else:
            return "just now"
        
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
