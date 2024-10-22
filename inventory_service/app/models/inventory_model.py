from sqlmodel import SQLModel, Field, Relationship

# Inventory Microservice Models
class InventoryItem(SQLModel, table=True):
    id: int  = Field(default=None, primary_key=True)
    product_id: int
    quantity: int
    name : str
    # variant_id: int | None = None
    
    # status: str 


class InventoryItemUpdate(SQLModel):
    quantity: int | None = None
    name : str | None = None
