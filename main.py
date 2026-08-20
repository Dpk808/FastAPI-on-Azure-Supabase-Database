from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session
import os

app = FastAPI(title="Inventory API")

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
allowed_origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]
cors_origin_regex = os.getenv("CORS_ORIGIN_REGEX")

# CORS Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=cors_origin_regex,
    allow_methods=["*"],
    allow_headers=["*"],
)

products = [
    Product(id=1, name="phone", description="budget phone", price=799, quantity=8),
    Product(id=2, name="laptop", description="gaming laptop", price=999, quantity=10),
    Product(id=3, name="tablet", description="study tablet", price=599, quantity=8),
    Product(id=4, name="Table", description="office table", price=299, quantity=10)

]   

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    try:
        count = db.query(database_models.Product).count()

        if count == 0:
            for product in products:
                db.add(database_models.Product(**product.model_dump()))

            db.commit()
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    database_models.Base.metadata.create_all(bind=engine)
    init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    # database connection 
 
    db_products = db.query(database_models.Product).all() 
     

    return db_products 

@app.get("/")
def greet():
    return "Welcome to my Site!!! " 


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return {"error": "Product not found"}
 
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()

    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated!"
    else:    
        return "Product not found"    


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted!"
    else:    
        return "Product not found"    

     
