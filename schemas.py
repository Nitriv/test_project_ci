from pydantic import BaseModel, ConfigDict, Field


class RecipeBookIn(BaseModel):
    """Схема для создания рецепта."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Название рецепта",
        examples=["Борщ"],
    )
    cooking_time: int = Field(
        ..., gt=0, description="Время готовки в минутах", examples=[90]
    )
    list_of_ingredients: list[str] = Field(
        ...,
        min_length=1,
        description="Список ингредиентов",
        examples=[["свёкла", "капуста", "говядина"]],
    )

    text_description: str | None = Field(
        None, description="Текстовое описание приготовления"
    )


class RecipeBookOut(BaseModel):
    """Схема ответа — краткая."""

    id: int = Field(..., description="id рецепта")
    title: str = Field(..., description="Название рецепта", examples=["Борщ"])
    cooking_time: int = Field(..., description="Время готовки в минутах", examples=[90])
    number_of_views: int = Field(..., description="Кол-во просмотров данного рецепта")

    model_config = ConfigDict(from_attributes=True)


class RecipeBookOutDetailed(RecipeBookOut):
    """Расширенная схема — все поля."""

    list_of_ingredients: list[str] = Field(
        ...,
        description="Список ингредиентов",
        examples=[["свёкла", "капуста", "говядина"]],
    )
    text_description: str | None = Field(
        ..., description="Текстовое описание приготовления"
    )
