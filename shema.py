from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuResponse(MenuBase):
    id: int


class SubMenuBase(BaseModel):

    title: str
    description: str

    class Config:
        orm_mode = True


class SubMenuResponse(SubMenuBase):
    id: int
    menu_id: int
    dishes_count: int


class DishesBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Dish_add(DishesBase):
    price: float


class DishesResponse(DishesBase):
    id: str
    price: str

