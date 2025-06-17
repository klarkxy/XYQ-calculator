# 人族门派
human_sects = ["女儿村", "方寸山", "天机城", "神木林", "大唐官府", "化生寺"]
# 魔族门派
demon_sects = ["盘丝洞", "阴曹地府", "狮驼岭", "无底洞", "魔王寨", "女魃墓"]
# 仙族门派
immortal_sects = ["普陀山", "花果山", "五庄观", "天宫", "龙宫", "凌波城"]


# 定义不同种族的属性成长
def get_attribute_growth(race):
    """
    根据种族返回对应的属性成长字典。
    """
    growth = {}
    # 仙族属性成长
    if race == "仙族":
        growth = {
            "体质": {"气血": 4.5, "速度": 0.1, "灵力": 0.3},
            "魔力": {"魔法": 3.5, "灵力": 0.7},
            "力量": {"命中": 1.7, "伤害": 0.6, "速度": 0.1, "灵力": 0.4},
            "耐力": {"防御": 1.6, "速度": 0.1, "灵力": 0.2},
            "敏捷": {"速度": 0.7, "躲避": 1.0},
        }
    # 人族属性成长
    elif race == "人族":
        growth = {
            "体质": {"气血": 5.0, "速度": 0.1, "灵力": 0.3},
            "魔力": {"魔法": 3.0, "灵力": 0.7},
            "力量": {"命中": 2.0, "伤害": 0.7, "速度": 0.1, "灵力": 0.4},
            "耐力": {"防御": 1.5, "速度": 0.1, "灵力": 0.2},
            "敏捷": {"速度": 0.7, "躲避": 1.0},
        }
    # 魔族属性成长
    elif race == "魔族":
        growth = {
            "体质": {"气血": 6.0, "速度": 0.1, "灵力": 0.3},
            "魔力": {"魔法": 2.5, "灵力": 0.7},
            "力量": {"命中": 2.3, "伤害": 0.7, "速度": 0.1, "灵力": 0.4},
            "耐力": {"防御": 1.4, "速度": 0.1, "灵力": 0.2},
            "敏捷": {"速度": 0.7, "躲避": 1.0},
        }
    return growth


# 根据门派设定种族
def get_race_by_sect(sect):
    """
    根据门派名称返回对应的种族。
    """

    if sect in human_sects:
        return "人族"
    elif sect in demon_sects:
        return "魔族"
    elif sect in immortal_sects:
        return "仙族"
    else:
        return "未知门派"


# 计算属性加成
def calculate_attribute_bonus(race, 体质, 魔力, 力量, 耐力, 敏捷):
    """
    根据种族和属性点计算各项属性加成。
    返回一个字典，包含气血、魔法、命中、伤害、防御、速度、躲避、灵力等属性的加成。
    """
    growth = get_attribute_growth(race)
    bonus = {
        "气血": 0,
        "魔法": 0,
        "命中": 0,
        "伤害": 0,
        "防御": 0,
        "速度": 0,
        "躲避": 0,
        "灵力": 0,
    }

    # 根据体质属性计算加成
    if "体质" in growth:
        bonus["气血"] += 体质 * growth["体质"].get("气血", 0)
        bonus["速度"] += 体质 * growth["体质"].get("速度", 0)
        bonus["灵力"] += 体质 * growth["体质"].get("灵力", 0)
    # 根据魔力属性计算加成
    if "魔力" in growth:
        bonus["魔法"] += 魔力 * growth["魔力"].get("魔法", 0)
        bonus["灵力"] += 魔力 * growth["魔力"].get("灵力", 0)
    # 根据力量属性计算加成
    if "力量" in growth:
        bonus["命中"] += 力量 * growth["力量"].get("命中", 0)
        bonus["伤害"] += 力量 * growth["力量"].get("伤害", 0)
        bonus["速度"] += 力量 * growth["力量"].get("速度", 0)
        bonus["灵力"] += 力量 * growth["力量"].get("灵力", 0)
    # 根据耐力属性计算加成
    if "耐力" in growth:
        bonus["防御"] += 耐力 * growth["耐力"].get("防御", 0)
        bonus["速度"] += 耐力 * growth["耐力"].get("速度", 0)
        bonus["灵力"] += 耐力 * growth["耐力"].get("灵力", 0)
    # 根据敏捷属性计算加成
    if "敏捷" in growth:
        bonus["速度"] += 敏捷 * growth["敏捷"].get("速度", 0)
        bonus["躲避"] += 敏捷 * growth["敏捷"].get("躲避", 0)

    return bonus


# 计算实际伤害
def calculate_actual_damage(weapon_命中, weapon_伤害, strength_伤害):
    """
    计算实际伤害。
    公式：武器命中/3 + 武器伤害 + 力量伤害
    """
    return weapon_命中 / 3 + weapon_伤害 + strength_伤害


# 计算实际法伤
def calculate_actual_spell_damage(weapon_伤害, spirit_power):
    """
    计算实际法伤。
    公式：武器伤害/4 + 属性带来的灵力
    """
    return weapon_伤害 / 4 + spirit_power


# 计算固伤
def calculate_fixed_damage(sect, weapon_伤害, 敏捷, actual_damage):
    """
    计算固伤。
    根据门派和公式计算固伤。
    """
    fixed_damage = 0
    # 女儿村固伤计算
    if sect == "女儿村":
        fixed_damage = weapon_伤害 * 0.18 + 敏捷 * 0.5
    # 无底洞固伤计算
    elif sect == "无底洞":
        fixed_damage = weapon_伤害 * 0.125 * 2 + 敏捷 * 0.7
    # 阴曹地府固伤计算
    elif sect == "阴曹地府":
        fixed_damage = weapon_伤害 * 0.15 + 敏捷 * 0.35
    # 普陀山固伤计算
    elif sect == "普陀山":
        fixed_damage = weapon_伤害 * 0.24 + 敏捷 * 0.7
    # 盘丝洞固伤计算
    elif sect == "盘丝洞":
        fixed_damage = weapon_伤害 * 0.18 + actual_damage / 3
    # 天机城固伤计算
    elif sect == "天机城":
        fixed_damage = weapon_伤害 * 0.18 + actual_damage / 3
    return fixed_damage


def calculate_all_attributes(sect, 命中, 伤害, 力量, 耐力, 敏捷, 体质, 魔力):
    """
    总入口函数，计算所有相关属性和伤害，并返回一个字典。
    参数:
        sect (str): 门派
        命中 (float): 命中
        伤害 (float): 伤害
        力量 (float): 力量
        耐力 (float): 耐力
        敏捷 (float): 敏捷
        体质 (float): 体质
        魔力 (float): 魔力
    返回:
        dict: 包含计算结果的字典
    """
    # 根据门派获取种族
    race = get_race_by_sect(sect)
    # 计算属性加成
    attribute_bonus = calculate_attribute_bonus(race, 体质, 魔力, 力量, 耐力, 敏捷)
    # 计算实际伤害
    actual_damage = calculate_actual_damage(命中, 伤害, attribute_bonus["伤害"])
    # 计算实际法伤
    actual_spell_damage = calculate_actual_spell_damage(伤害, attribute_bonus["灵力"])
    # 计算固伤
    fixed_damage = calculate_fixed_damage(sect, 伤害, 敏捷, actual_damage)

    # 组织计算结果
    results = {
        "门派": sect,
        "种族": race,
        "属性加成": attribute_bonus,
        "实际伤害": actual_damage,
        "实际法伤": actual_spell_damage,
        "固伤": fixed_damage,
    }

    # 递归删除结果中所有的0属性
    def remove_zero_attributes(data):
        if not isinstance(data, dict):
            return data

        cleaned_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                processed_value = remove_zero_attributes(value)
                if len(processed_value) > 0:
                    cleaned_data[key] = processed_value
            elif isinstance(value, (int, float)):
                if value != 0:
                    cleaned_data[key] = value
            else:
                cleaned_data[key] = value

        return cleaned_data

    results = remove_zero_attributes(results)

    return results
