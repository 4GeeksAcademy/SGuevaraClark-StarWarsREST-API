from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#users, articles, tags, articlesTags
class ArticlesTags(db.Model):
    __tablename__ = 'articlestags'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable = False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable = False)
    extra_info = db.Column(db.Text)



class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    articles = db.relationship('Articles', backref='user')

    def __repr__(self):
        return '<Users %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tags', secondary='articlestags', backrefs='articles')
   
    def __repr__(self):
        return '<Articles %r>' % self.title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }


class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    posts = db.relationship('Posts', secondary='articlestags', backrefs='tags')


    def __repr__(self):
        return '<Tags %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

