"""Join table between Announcement and User entities."""

from sqlalchemy import Table, Column, ForeignKey, Integer
from .entity_base import EntityBase

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Define association table for upvotes (many-to-many relationship)
announcement_upvote_table = Table(
    "announcement_upvotes",
    EntityBase.metadata,
    Column("announcement_id", Integer, ForeignKey("announcement.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
)

announcement_favorite_table = Table(
    "announcement_favorites",
    EntityBase.metadata,
    Column("announcement_id", Integer, ForeignKey("announcement.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
)
