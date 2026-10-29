from sqlalchemy import Column, String, Integer, JSON

from database import Base

class RecipeBook(Base):
    __tablename__ = 'recipe_books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    cooking_time = Column(Integer, index=True, nullable=False)
    list_of_ingredients = Column(JSON, nullable=False)
    text_description = Column(String)
    number_of_views = Column(Integer, index=True, default=0, server_default='0')
