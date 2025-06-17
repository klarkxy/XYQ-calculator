# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
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

    def build(self):
        """
        构建应用程序界面。
        """
        # 初始化时添加一个默认武器
        self.weapon_list.append(WeaponData())
        self.current_weapon = self.weapon_list[0]

        # 主布局
        main_layout = BoxLayout(orientation="vertical")

        # 顶部区域：门派选择和添加按钮
        top_layout = BoxLayout(size_hint_y=0.1)
        factions = human_sects + demon_sects + immortal_sects
        self.faction_spinner = Spinner(
            text="选择门派",
            values=factions,
            size_hint=(0.5, None),
            height=40,
            font_name=DEFAULT_FONT,
        )
        # 绑定门派选择事件
        self.faction_spinner.bind(text=self.on_faction_select)
        faction_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40
        )
        faction_layout.add_widget(self.faction_spinner)
        main_layout.add_widget(faction_layout)

        # 底部区域：列表、表单、输出
        bottom_layout = BoxLayout(orientation="horizontal", size_hint_y=1)

        # 左侧区域：武器列表
        left_layout = BoxLayout(orientation="vertical", size_hint_x=0.3, size_hint_y=1)
        add_button = Button(
            text="新增武器", size_hint_y=None, height=40, font_name=DEFAULT_FONT
        )
        # 绑定新增武器按钮事件
        add_button.bind(on_press=self.add_weapon)
        left_layout.add_widget(add_button)
        left_layout.add_widget(Label(text="武器列表", font_name=DEFAULT_FONT))
        # RecycleView 的占位符，用于显示武器列表
        self.weapon_recycleview = RecycleView(
            data=[{"text": x.name, "font_name": DEFAULT_FONT} for x in self.weapon_list]
        )
        self.weapon_recycleview.viewclass = "Button"
        # 简单的绑定，用于选择武器
        self.weapon_recycleview.bind(on_touch_down=self.on_weapon_select)
        left_layout.add_widget(self.weapon_recycleview)
        bottom_layout.add_widget(left_layout)

        # 中间区域：属性表单
        middle_layout = BoxLayout(orientation="vertical", size_hint_x=0.4)
        middle_layout.add_widget(Label(text="武器属性", font_name=DEFAULT_FONT))
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
        right_layout.add_widget(Label(text="计算结果", font_name=DEFAULT_FONT))
        self.output_label = Label(text=self.output_text, font_name=DEFAULT_FONT)
        right_layout.add_widget(self.output_label)
        bottom_layout.add_widget(right_layout)

        main_layout.add_widget(bottom_layout)

        # 初始化时更新表单和计算结果
        self.update_form()
        self.calculate_equivalent_damage()

        return main_layout

    def on_faction_select(self, instance, value):
        """
        处理门派选择事件。
        """
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

    def on_weapon_select(self, instance, touch):
        """
        处理武器列表选择事件。
        """
        # RecycleView 的简单选择逻辑
        if instance.collide_point(*touch.pos):
            for index, item in enumerate(self.weapon_recycleview.data):
                # 检查触摸是否在列表项的边界内
                if (
                    self.weapon_recycleview.children
                    and self.weapon_recycleview.children[0].children
                ):
                    list_item_widgets = self.weapon_recycleview.children[0].children
                    # RecycleView 项从底部向上添加，因此反转索引
                    widget_index = len(list_item_widgets) - 1 - index
                    if 0 <= widget_index < len(list_item_widgets):
                        if list_item_widgets[widget_index].collide_point(*touch.pos):
                            # 设置当前武器为选中的武器
                            self.current_weapon = self.weapon_list[index]
                            # 更新表单和计算结果
                            self.update_form()
                            self.calculate_equivalent_damage()
                            break

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

    def calculate_equivalent_damage(self):
        """
        计算武器的等效伤害并更新输出。
        """
        if self.current_weapon and self.faction_spinner.text != "选择门派":
            faction = self.faction_spinner.text
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
