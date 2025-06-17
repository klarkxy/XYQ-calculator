# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from calculator_logic import (
    calculate_all_attributes,
    human_sects,
    demon_sects,
    immortal_sects,
)

# 注册自定义字体
LabelBase.register(DEFAULT_FONT, fn_regular="sarasa-mono-sc-nerd-regular.ttf")


class WeaponData:
    """
    存储武器属性数据的类。
    """

    def __init__(
        self,
        name="新武器",
        hit=0,
        damage=0,
        constitution=0,
        magic=0,
        strength=0,
        endurance=0,
        agility=0,
    ):
        """
        初始化 WeaponData 对象。

        Args:
            name (str): 武器名称。
            hit (int): 命中属性。
            damage (int): 伤害属性。
            constitution (int): 体质属性。
            magic (int): 魔力属性。
            strength (int): 力量属性。
            endurance (int): 耐力属性。
            agility (int): 敏捷属性。
        """
        self.name = name
        self.hit = hit
        self.damage = damage
        self.constitution = constitution
        self.magic = magic
        self.strength = strength
        self.endurance = endurance
        self.agility = agility


class CalculatorApp(App):
    """
    武器计算器 Kivy 应用程序类。
    """

    weapon_list = ListProperty([])  # 武器列表
    current_weapon = ObjectProperty(None)  # 当前选中的武器
    output_text = StringProperty("")  # 计算结果输出文本
    selected_faction = StringProperty(None, allow_none=True)  # 当前选中的门派

    def build(self):
        """
        构建应用程序界面。
        """
        # 初始化时添加一个默认武器
        self.weapon_list.append(WeaponData())
        self.current_weapon = self.weapon_list[0]

        # 主布局
        main_layout = BoxLayout(orientation="vertical")

        # 顶部区域：门派选择（按种族分组，3列）

        faction_layout = BoxLayout(orientation="vertical", size_hint_y=0.2)

        # 使用 GridLayout 实现三列布局
        grid_layout = GridLayout(cols=3, size_hint_y=1)

        # 添加人族门派
        grid_layout.add_widget(Label(text="人族", font_name=DEFAULT_FONT))
        grid_layout.add_widget(Label(text="魔族", font_name=DEFAULT_FONT))
        grid_layout.add_widget(Label(text="仙族", font_name=DEFAULT_FONT))

        # 添加门派按钮
        all_sects = [human_sects, demon_sects, immortal_sects]
        self.faction_buttons = {}  # 存储门派按钮
        for i in range(max(len(human_sects), len(demon_sects), len(immortal_sects))):
            for j, sects in enumerate(all_sects):
                if i < len(sects):
                    sect_name = sects[i]
                    btn = Button(text=sect_name, font_name=DEFAULT_FONT)
                    btn.bind(on_press=self.on_faction_button_press)
                    self.faction_buttons[sect_name] = btn
                    grid_layout.add_widget(btn)
                else:
                    # 添加一个空的部件以保持列对齐
                    grid_layout.add_widget(Label())

        faction_layout.add_widget(grid_layout)
        main_layout.add_widget(faction_layout)

        # 分隔线
        separator = BoxLayout(size_hint_y=None, height=5)
        main_layout.add_widget(separator)

        # 底部区域：列表、表单、输出
        bottom_layout = BoxLayout(orientation="horizontal", size_hint_y=0.8)

        # 左侧区域：武器列表
        left_layout = BoxLayout(orientation="vertical", size_hint_x=0.3, size_hint_y=1)
        add_button = Button(
            text="新增武器", size_hint_y=None, height=40, font_name=DEFAULT_FONT
        )
        # 绑定新增武器按钮事件
        add_button.bind(on_press=self.add_weapon)
        left_layout.add_widget(add_button)
        # 创建一个可滚动的武器列表
        self.weapon_recycleview = RecycleView(
            scroll_type=["bars", "content"],
            bar_width=10,
            scroll_wheel_distance=20,
        )
        # 创建 RecycleBoxLayout 作为布局管理器并添加为子部件
        recycle_box_layout = RecycleBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            default_size_hint=(1, None),
            default_size=(None, 40),
        )
        self.weapon_recycleview.add_widget(recycle_box_layout)
        self.weapon_recycleview.viewclass = "Button"
        self.weapon_recycleview.data = [
            {
                "text": x.name,
                "font_name": DEFAULT_FONT,
                "on_release": lambda instance, idx=i: self.select_weapon(idx),
            }
            for i, x in enumerate(self.weapon_list)
        ]

        left_layout.add_widget(self.weapon_recycleview)
        bottom_layout.add_widget(left_layout)

        # 中间区域：属性表单
        middle_layout = BoxLayout(orientation="vertical", size_hint_x=0.4)

        # 添加武器名称输入框
        name_layout = BoxLayout(size_hint_y=0.1)
        name_layout.add_widget(
            Label(text="武器名称", size_hint_x=0.4, font_name=DEFAULT_FONT)
        )
        self.name_input = TextInput(
            multiline=False,
            size_hint_x=0.6,
            font_name=DEFAULT_FONT,
        )
        # 绑定武器名称输入框文本变化事件
        self.name_input.bind(text=self.on_name_change)
        name_layout.add_widget(self.name_input)
        middle_layout.add_widget(name_layout)

        self.attribute_inputs = {}  # 存储属性输入框
        attributes = ["命中", "伤害", "体质", "魔力", "力量", "耐力", "敏捷"]
        for attr in attributes:
            attr_layout = BoxLayout(size_hint_y=0.1)
            attr_layout.add_widget(
                Label(text=attr, size_hint_x=0.4, font_name=DEFAULT_FONT)
            )
            text_input = TextInput(
                input_type="number",
                multiline=False,
                size_hint_x=0.6,
                font_name=DEFAULT_FONT,
            )
            # 绑定属性输入框文本变化事件
            text_input.bind(text=self.on_attribute_change)
            self.attribute_inputs[attr] = text_input  # 使用中文属性名作为键
            attr_layout.add_widget(text_input)
            middle_layout.add_widget(attr_layout)
        bottom_layout.add_widget(middle_layout)

        # 右侧区域：输出
        right_layout = BoxLayout(orientation="vertical", size_hint_x=0.3)
        self.output_label = Label(text=self.output_text, font_name=DEFAULT_FONT)
        right_layout.add_widget(self.output_label)
        bottom_layout.add_widget(right_layout)

        main_layout.add_widget(bottom_layout)

        # 初始化时更新表单和计算结果
        self.update_form()
        self.calculate_equivalent_damage()

        return main_layout

    def on_name_change(self, instance, value):
        """
        处理武器名称输入框文本变化事件。
        """
        if self.current_weapon:
            self.current_weapon.name = value
            # 更新 RecycleView 数据以反映名称变化
            self.weapon_recycleview.data = [
                {"text": x.name, "font_name": DEFAULT_FONT} for x in self.weapon_list
            ]
        self.calculate_equivalent_damage()

    def on_faction_button_press(self, instance):
        """
        处理门派按钮点击事件。
        """
        # 获取被点击按钮的文本（门派名称）
        faction = instance.text
        # 更新当前选中的门派
        self.selected_faction = faction
        # 更新计算结果
        self.calculate_equivalent_damage()

    def add_weapon(self, instance):
        """
        处理新增武器按钮事件。
        """
        # 创建新的武器数据
        new_weapon = WeaponData(name=f"新武器 {len(self.weapon_list) + 1}")
        self.weapon_list.append(new_weapon)
        # 更新 RecycleView 数据
        self.weapon_recycleview.viewclass = "Button"
        self.weapon_recycleview.data = [
            {"text": x.name, "font_name": DEFAULT_FONT} for x in self.weapon_list
        ]
        # 设置当前武器为新添加的武器
        self.current_weapon = new_weapon
        # 更新表单和计算结果
        self.update_form()
        self.calculate_equivalent_damage()

    def on_attribute_change(self, instance, value):
        """
        处理属性输入框文本变化事件。
        """
        # 根据表单输入更新当前武器数据
        # 查找哪个属性输入触发了更改
        chinese_attr = None
        for key, input_widget in self.attribute_inputs.items():
            if input_widget == instance:
                chinese_attr = key
                break

        if chinese_attr:
            try:
                # 使用 setattr 更新武器属性
                setattr(
                    self.current_weapon,
                    # 将中文属性名映射到英文变量名
                    {
                        "命中": "hit",
                        "伤害": "damage",
                        "体质": "constitution",
                        "魔力": "magic",
                        "力量": "strength",
                        "耐力": "endurance",
                        "敏捷": "agility",
                    }.get(
                        chinese_attr, chinese_attr
                    ),  # 如果找不到映射，使用原中文名（应避免）
                    float(value) if value else 0,
                )
            except ValueError:
                pass  # 如有必要，处理非数字输入

        # 重新计算等效伤害
        self.calculate_equivalent_damage()

    def update_form(self):
        """
        根据当前武器数据更新表单输入框。
        """
        # 根据当前武器数据更新表单输入
        if self.current_weapon:
            self.name_input.text = self.current_weapon.name
            for chinese_attr, input_widget in self.attribute_inputs.items():
                # 将中文属性名映射到英文变量名以获取属性值
                english_attr = {
                    "命中": "hit",
                    "伤害": "damage",
                    "体质": "constitution",
                    "魔力": "magic",
                    "力量": "strength",
                    "耐力": "endurance",
                    "敏捷": "agility",
                }.get(
                    chinese_attr, chinese_attr
                )  # 如果找不到映射，使用原中文名（应避免）
                input_widget.text = str(getattr(self.current_weapon, english_attr))

    def calculate_equivalent_damage(self, faction=None):
        """
        计算武器的等效伤害并更新输出。
        """
        # 如果没有传入门派，使用当前选中的门派
        if faction is None:
            faction = self.selected_faction

        if self.current_weapon and faction:
            # 调用 calculator_logic 中的函数进行计算
            results = calculate_all_attributes(
                faction,
                self.current_weapon.hit,
                self.current_weapon.damage,
                self.current_weapon.strength,
                self.current_weapon.endurance,
                self.current_weapon.agility,
                self.current_weapon.constitution,
                self.current_weapon.magic,
            )

            # 格式化输出文本
            output = f"门派: {results['门派']}\n"
            output += f"种族: {results['种族']}\n"
            output += f"武器: {self.current_weapon.name}\n"
            output += "\n计算结果:\n"
            output += f"  伤害: {results['实际伤害']:.2f}\n"
            output += f"  法伤: {results['实际法伤']:.2f}\n"
            output += f"  固伤: {results['固伤']:.2f}\n"
            output += "  属性加成:\n"
            for attr, value in results["属性加成"].items():
                output += f"    {attr}: {value:.2f}\n"

            self.output_text = output
            self.output_label.text = self.output_text
        else:
            # 如果未选择门派或武器，显示提示信息
            self.output_text = "请选择门派并输入武器属性进行计算。"
            self.output_label.text = self.output_text


if __name__ == "__main__":
    # 运行应用程序
    CalculatorApp().run()
