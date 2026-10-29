from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, Query
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from database import get_session, lifespan

# uvicorn main:app --reload

app = FastAPI(
    title="Кулинарная книга",
    description="Очень хорошая кулинарная книга. Высший вкус",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get(
    "/recipes/",
    response_model=list[schemas.RecipeBookOut],
    summary="Краткий список всех рецептов",
    description=(
            "Возвращает постранично список всех рецептов, "
            "отсортированных по популярности."
    ),
    responses={422: {"description": "Некорректные параметры пагинации"}},
)
async def recipes(
    db: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[
        int, Query(ge=1, le=100, description="Сколько записей вернуть")
    ] = 20,
    offset: Annotated[int, Query(ge=0, description="Сколько записей пропустить")] = 0,
):
    stmt = (
        select(models.RecipeBook)
        .order_by(
            models.RecipeBook.number_of_views.desc(),
            models.RecipeBook.cooking_time,
        )
        .limit(limit)
        .offset(offset)
    )

    res = await db.execute(stmt)
    return res.scalars().all()


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeBookOutDetailed,
    summary="Детальная информация о рецепте",
    description="Возвращает рецепт целиком и увеличивает счётчик просмотров на 1.",
    responses={404: {"description": "Рецепт не найден"}},
)
async def get_recipe(
    recipe_id: Annotated[int, Path(description="Идентификатор рецепта", ge=1)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    recipe = await db.get(models.RecipeBook, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    await db.execute(
        update(models.RecipeBook)
        .where(models.RecipeBook.id == recipe_id)
        .values(number_of_views=models.RecipeBook.number_of_views + 1)
    )
    await db.commit()
    await db.refresh(recipe)
    return recipe


@app.post(
    "/recipes/",
    response_model=schemas.RecipeBookOut,
    status_code=201,
    summary="Внести новый рецепт",
    description=(
            "Создаёт новый рецепт. Возвращает объект с присвоенным id "
            "и нулевым счётчиком просмотров."
    ),
    responses={422: {"description": "Ошибка валидации входных данных"}},
)
async def add_recipes(
    recipe: schemas.RecipeBookIn, db: Annotated[AsyncSession, Depends(get_session)]
):
    new_recipe = models.RecipeBook(**recipe.model_dump())
    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    return new_recipe
