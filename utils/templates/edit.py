from disnake import (
    ui,
    Locale,
    ButtonStyle,
    SelectOption,
    MediaGalleryItem,
)


def edit_member_quartz_template(author_id: int) -> ui.UIComponent: 
    return [
        ui.Container(
            ui.TextDisplay("Выберите пользователя:"),
            ui.ActionRow(
                ui.UserSelect(
                    custom_id=f"edit_member_quartz_user:{author_id}",
                    min_values=1,
                    max_values=1,
                )
            ),
            ui.Separator(),
            ui.TextDisplay("Выберите тип кварца:"),
            ui.ActionRow(
                ui.StringSelect(
                    custom_id=f"edit_member_quartz_type:{author_id}",
                    options=[
                        SelectOption(label="Обычный", value="quartz"),
                        SelectOption(label="Негатив", value="negative_quartz"), 
                        SelectOption(label="Золотой", value="gold_quartz"), 
                    ],
                    min_values=1,
                    max_values=1,
                )
            ),
            ui.Separator(),
            ui.TextDisplay("Выберите количество:"),
            ui.ActionRow(
                ui.StringSelect(
                    custom_id=f"edit_member_quartz_value:{author_id}",
                    options=[
                        SelectOption(label="1", value="1", description="Адин"),
                        SelectOption(label="5", value="5", description="Пят"),
                        SelectOption(label="10", value="10", description="Десат"),
                    ],
                    max_values=1,
                    min_values=1,
                )
            ),
            ui.Separator(),
            ui.TextDisplay("Выберите задачу:"),
            ui.ActionRow(
                ui.StringSelect(
                    custom_id=f"edit_member_quartz_request:{author_id}", 
                    options=[
                        SelectOption(label="Добавить", value="add"), 
                        SelectOption(label="Отнять", value="remove"), 
                    ]
                )
            ),
            ui.Separator(),
            ui.ActionRow(
                ui.Button(
                    label="Подтвердить", 
                    custom_id=f"edit_member_quartz_confirm:{author_id}", 
                    style=ButtonStyle.primary, 
                )
            )
        )
    ]
