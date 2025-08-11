from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(50), default="0", nullable=True)  # Optional rating
    link = db.Column(db.String(500), nullable=False, unique=True)
    image = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    search_keyword = db.Column(db.String(100), nullable=False)  # NEW column

    def __repr__(self):
        return f"<Product {self.title} from {self.source}>"
