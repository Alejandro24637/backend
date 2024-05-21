from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"],
                   responses={404: {"message":"No encontrado"} })

list_products = ["Cereal","Platos","Vasos","Arroz","Pollo"]

@router.get("/")
async def products():
    return list_products

@router.get("/{id}")
async def products(id : int):
    return list_products[id]