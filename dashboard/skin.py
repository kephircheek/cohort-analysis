from collections import OrderedDict
STATUS_LINE = {
    "label": "Когортный анaлиз"
}

DASHBOARD = {
    "submit": "Построить графики",
    "controls": OrderedDict([
        (
            "cohort_type",
            {
                "label": "Тип когорты",
                "options": OrderedDict([
                    ("Дата первого посещения", "JoinMonth"),
                ])
            }
        ),
        (
            "cohort_range",
            {
                "label": "Размер когорты",
                "options": OrderedDict([
                    ("по месяцам", "month")
                ])
            }
        ),
        (
            "target", {
                "label": "Показатель",
                "options": OrderedDict([
                    ("Пользователей", 'users')
                ])
            }
        ),
        (
            "date_range", {
                "label": "Диапозон дат",
                "options": OrderedDict([
                    ("За последний месяц", "month") ,
                    ("За квартал", 'quarter'),
                    ("За полгода", 'half-year'),
                    ("За год", 'year')
                ])
            }
        )

    ])
}
