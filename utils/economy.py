from settings import conf

def normalize_value(value: float) -> float: 
    return round(max(value, 0.00), 2)


def get_money_draw(value: float, type: str) -> str: 
    return f"{value}{conf.quartz_emojis[conf.quartz_types.get(type, 'quartz')]}"