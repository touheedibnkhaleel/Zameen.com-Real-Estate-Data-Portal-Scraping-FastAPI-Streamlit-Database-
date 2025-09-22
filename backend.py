from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from database import engine,get_db
from fastapi import Query
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get('/properties')
def get_PropertyDetails(db:Session = Depends(get_db)):
    details = db.query(models.PropertyDetails).all()
    return details


@app.get("/properties/search")
def search_properties(
    location: str = Query(None),
    type: str = Query(None),  
    min_price: int = Query(None),
    max_price: int = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.PropertyDetails)

    if location:
        query = query.filter(models.PropertyDetails.location.ilike(f"%{location}%"))
    if type:
        query = query.filter(models.PropertyDetails.property_type.ilike(f"%{type}%"))  
    if min_price:
        query = query.filter(models.PropertyDetails.price >= min_price)
    if max_price:
        query = query.filter(models.PropertyDetails.price <= max_price)

    results = query.all()
    return {"count": len(results), "data": results}


@app.get('/properties/{id}')
def get_one_PropertyDetails(id : int ,db : Session = Depends(get_db)):
    details = db.query(models.PropertyDetails).filter(models.PropertyDetails.id == id).first()
    return details
