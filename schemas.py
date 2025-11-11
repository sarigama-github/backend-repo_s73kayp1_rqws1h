"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Boosting service specific schemas

class Order(BaseModel):
    """
    Orders collection schema
    Collection name: "order"
    """
    game: str = Field(..., description="Game name e.g., Genshin Impact, Honkai: Star Rail")
    service: str = Field(..., description="Selected boosting service")
    quantity: int = Field(1, ge=1, description="Units for the service (e.g., floors, hours, levels)")
    priority: bool = Field(False, description="Rush order option")
    streaming: bool = Field(False, description="Live stream option")
    region: Optional[str] = Field(None, description="Server/region")
    username: Optional[str] = Field(None, description="Account username or UID")
    note: Optional[str] = Field(None, description="Additional details or requirements")
    contact_email: Optional[EmailStr] = Field(None, description="Customer email for updates")
    contact_discord: Optional[str] = Field(None, description="Customer Discord tag")
    price_estimate: float = Field(..., ge=0, description="Estimated price at time of order")
    status: str = Field("pending", description="Order status")

class Testimonial(BaseModel):
    """
    Testimonials collection schema
    Collection name: "testimonial"
    """
    name: str = Field(..., description="Customer name or alias")
    game: Optional[str] = Field(None, description="Game related to the review")
    rating: int = Field(5, ge=1, le=5, description="Star rating 1-5")
    comment: str = Field(..., description="Review content")
    highlights: Optional[List[str]] = Field(None, description="Key positives from the experience")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
