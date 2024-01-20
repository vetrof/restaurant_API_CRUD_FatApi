@menu_router.get('/menus/')
def get_menus(db: Session = Depends(get_db)):
    menus = db.query(Menu).all()
    if menus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    menu_list = [{'id': str(menu.id),
                  'title': menu.title,
                  'description': menu.description} for menu in menus]
    return menu_list


@menu_router.get("/menus/{menu_id}", response_model=ResponseMenuSchema)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    menu_data = {'id': str(menu.id), 'title': menu.title, 'description': menu.description}
    return menu_data


@menu_router.post("/menus/", response_model=ResponseMenuSchema, status_code=status.HTTP_201_CREATED)
def create_menu(item: MenuSchema, db: Session = Depends(get_db)):
    menu = Menu(title=item.title, description=item.description)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    menu_data = {'id': str(menu.id), 'title': menu.title, 'description': menu.description}
    return menu_data


@menu_router.patch("/menus/{menu_id}", response_model=ResponseMenuSchema)
def update_menu(menu_id: int, item: MenuSchema, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    menu.title = item.title
    menu.description = item.description
    db.commit()
    db.refresh(menu)
    menu_data = {'id': str(menu.id), 'title': menu.title, 'description': menu.description}

    return menu_data


@menu_router.delete("/menus/{menu_id}", status_code=status.HTTP_200_OK)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    db.delete(menu)
    db.commit()
    menu_data = {'id': menu.id, 'title': menu.title, 'description': menu.description}
    return menu_data