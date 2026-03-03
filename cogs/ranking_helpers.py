from decimal import Decimal, ROUND_HALF_UP


CATACOMBS_BASE_TABLE = [
    50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940,
    12700, 17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140,
    259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640,
    3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640,
    23159640, 30359640, 39559640, 51559640, 66559640, 85559640, 109559640,
    139559640, 177559640, 225559640, 285559640, 360559640, 453559640,
    569809640,
]


def build_catacombs_level_table(extra_levels: int = 70, extra_xp: int = 200000000) -> list[int]:
    table = CATACOMBS_BASE_TABLE.copy()
    for _ in range(extra_levels):
        table.append(table[-1] + extra_xp)
    return table


def format_bmk(value) -> str:
    if value >= 1000000000000:
        return f"{Decimal(str(float(value / 1000000000000))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}T"
    if value >= 1000000000:
        return f"{Decimal(str(float(value / 1000000000))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}B"
    if value >= 1000000:
        return f"{Decimal(str(float(value / 1000000))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}M"
    if value >= 1000:
        return f"{Decimal(str(float(value / 1000))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}K"
    return str(value)


def count_golden_dragons(member_data: dict) -> tuple[int, int, int]:
    normal_count = 0
    lv200_count = 0
    lv100_count = 0
    for pet in member_data.get("pets", []):
        if pet.get("type") != "GOLDEN_DRAGON":
            continue
        exp = pet.get("exp", 0)
        if exp >= 210255385:
            lv200_count += 1
        elif exp >= 25353230:
            lv100_count += 1
        else:
            normal_count += 1
    return normal_count, lv200_count, lv100_count


def escape_rank_name(name: str) -> str:
    return name.replace("_", "\\_")
