from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models import Menu, Submenu, Dish
from database import engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

from shema import MenuBase, MenuResponse, SubMenuBase, SubMenuResponse, DishesBase, DishesResponse, Dish_add

from sqlalchemy.orm import Session

from sqlalchemy import func

app = FastAPI()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        # *** MENU ***


@app.get('/api/v1/menus', response_model=list[MenuResponse], tags=['Menu'])
def get_menus(db: Session = Depends(get_db)):
    menus = db.query(Menu).all()
    return menus


@app.get('/api/v1/menus/{menu_id}', response_model=MenuResponse, tags=['Menu'])
def get_menu_with_id(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter_by(id=menu_id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    # Подсчет количества подменю
    submenus_count = db.query(func.count(Submenu.id)).filter(Submenu.menu_id == menu_id).scalar()

    # Подсчет количества блюд
    dishes_count = db.query(func.count(Dish.id)).join(Submenu).filter(Submenu.menu_id == menu_id).scalar()

    return JSONResponse(status_code=status.HTTP_200_OK, content={'id': str(menu.id),
                                                                 'title': menu.title,
                                                                 'description': menu.description,
                                                                 'submenus_count': submenus_count,
                                                                 'dishes_count': dishes_count,
                                                                 })


@app.post("/api/v1/menus", response_model=MenuBase, tags=['Menu'])
def create_menu(new_menu: MenuBase, db: Session = Depends(get_db)):
    menu = Menu(title=new_menu.title, description=new_menu.description)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'id': str(menu.id),
                                                                      'title': menu.title,
                                                                      'description': menu.description})


@app.patch('/api/v1/menus/{menu_id}', response_model=MenuBase, tags=['Menu'])
def update_menu(menu_id: int, updated_menu: MenuBase, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter_by(id=menu_id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")

    menu.title = updated_menu.title
    menu.description = updated_menu.description
    db.commit()
    db.refresh(menu)
    return menu


@app.delete('/api/v1/menus/{menu_id}', tags=['Menu'])
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter_by(id=menu_id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")

    db.delete(menu)
    db.commit()
    return {'menu': 'deleted'}


#                                               *** SUB MENU ***

@app.get('/api/v1/menus/{menu_id}/submenus', tags=['Sub menu'])
def get_submenu_for_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Submenu).filter_by(menu_id=menu_id).all()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    return menu


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=SubMenuBase, tags=['Sub menu'])
def get_submenu_with_id(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter_by(id=submenu_id, menu_id=menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    dish_count = db.query(func.count(Dish.id)).filter(Dish.submenu_id == submenu_id).scalar()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'id': str(submenu.id),
                                 'title': submenu.title,
                                 'description': submenu.description,
                                 'dishes_count': dish_count})


@app.post('/api/v1/menus/{menu_id}/submenus', response_model=SubMenuResponse, tags=['Sub menu'])
def add_submenu(menu_id: int, submenu_new: SubMenuBase, db: Session = Depends(get_db)):
    submenu = Submenu(title=submenu_new.title, description=submenu_new.description, menu_id=menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={'id': str(submenu.id), 'title': submenu.title,
                                 'description': submenu.description})


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['Sub menu'])
def update_submenu(menu_id: int, submenu_id: int, submenu_update: SubMenuBase, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter_by(id=submenu_id, menu_id=menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    submenu.title = submenu_update.title
    submenu.description = submenu_update.description
    db.commit()
    db.refresh(submenu)
    return submenu


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['Sub menu'])
def update_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter_by(id=submenu_id, menu_id=menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    db.delete(submenu)
    db.commit()
    return {'menu': 'deleted'}


#                                               *** DISHES ***

@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dishes'])
def get_dishes_for_menu_and_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    dishes = db.query(Dish).filter(Dish.submenu_id == submenu_id).all()
    return dishes


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', tags=['Dishes'])
def get_dishes_submenu_with_id(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter_by(id=dish_id, submenu_id=submenu_id).first()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'id': str(dish.id),
                                 'title': dish.title,
                                 'description': dish.description,
                                 'price': str(dish.price)})


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=DishesResponse, tags=['Dishes'])
def add_dishes_submenu(menu_id: int, submenu_id: int, dish_new: Dish_add, db: Session = Depends(get_db)):
    dish = Dish(title=dish_new.title, description=dish_new.description, price=dish_new.price, submenu_id=submenu_id)
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={'id': str(dish.id),
                                 'title': dish.title,
                                 'description': dish.description,
                                 'price': str(dish.price)})


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', tags=['Dishes'])
def patch_dishes_submenu_with_id(menu_id: int, submenu_id: int, dish_id: int, dish_update: Dish_add,
                                 db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter_by(id=submenu_id, menu_id=menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu or menus not found")

    dish = db.query(Dish).filter_by(id=dish_id).first()
    dish.title = dish_update.title
    dish.description = dish_update.description
    dish.price = dish_update.price
    db.commit()
    db.refresh(dish)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'id': str(dish.id),
                                 'title': dish.title,
                                 'description': dish.description,
                                 'price': str(dish.price)})


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', tags=['Dishes'])
def delete_dishes_submenu_with_id(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):

    dish = db.query(Dish).filter_by(id=dish_id).first()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")

    db.delete(dish)
    db.commit()
    return {'dish': 'deleted'}
