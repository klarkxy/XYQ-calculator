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

# Register the custom font
LabelBase.register(DEFAULT_FONT, fn_regular="sarasa-mono-sc-nerd-regular.ttf")


class WeaponData:
    def __init__(
        self,
        名称="新武器",
        命中=0,
        伤害=0,
        体质=0,
        魔力=0,
        力量=0,
        耐力=0,
        敏捷=0,
    ):
        self.名称 = 名称
        self.命中 = 命中
        self.伤害 = 伤害
        self.体质 = 体质
        self.魔力 = 魔力
        self.力量 = 力量
        self.耐力 = 耐力
        self.敏捷 = 敏捷


class CalculatorApp(App):
    weapon_list = ListProperty([])
    current_weapon = ObjectProperty(None)
    output_text = StringProperty("")

    def build(self):
        self.weapon_list.append(WeaponData())
        self.current_weapon = self.weapon_list[0]

        # Main layout
        main_layout = BoxLayout(orientation="vertical")

        # Top area: Faction selection and Add button
        top_layout = BoxLayout(size_hint_y=0.1)
        factions = [
            "大唐官府",
            "方寸山",
            "龙宫",
            "普陀山",
            "女儿村",
            "天宫",
            "狮驼岭",
            "五庄观",
            "盘丝洞",
            "神木林",
            "魔王寨",
            "无底洞",
            "凌波城",
        ]
        self.faction_spinner = Spinner(
            text="选择门派",
            values=factions,
            size_hint=(0.5, None),
            height=40,
            font_name=DEFAULT_FONT,
        )
        self.faction_spinner.bind(text=self.on_faction_select)
        faction_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40
        )
        faction_layout.add_widget(self.faction_spinner)
        main_layout.add_widget(faction_layout)

        # Bottom area: List, Form, Output
        bottom_layout = BoxLayout(orientation="horizontal", size_hint_y=1)

        # Left area: Weapon list
        left_layout = BoxLayout(orientation="vertical", size_hint_x=0.3, size_hint_y=1)
        add_button = Button(
            text="新增武器", size_hint_y=None, height=40, font_name=DEFAULT_FONT
        )
        add_button.bind(on_press=self.add_weapon)
        left_layout.add_widget(add_button)
        left_layout.add_widget(Label(text="武器列表", font_name=DEFAULT_FONT))
        # Placeholder for RecycleView
        self.weapon_recycleview = RecycleView(
            data=[{"text": x.名称, "font_name": DEFAULT_FONT} for x in self.weapon_list]
        )
        self.weapon_recycleview.viewclass = "Button"
        self.weapon_recycleview.bind(
            on_touch_down=self.on_weapon_select
        )  # Simple binding for now
        left_layout.add_widget(self.weapon_recycleview)
        bottom_layout.add_widget(left_layout)

        # Middle area: Attribute form
        middle_layout = BoxLayout(orientation="vertical", size_hint_x=0.4)
        middle_layout.add_widget(Label(text="武器属性", font_name=DEFAULT_FONT))
        self.attribute_inputs = {}
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
            text_input.bind(text=self.on_attribute_change)
            self.attribute_inputs[attr] = (
                text_input  # Use Chinese attribute name as key
            )
            attr_layout.add_widget(text_input)
            middle_layout.add_widget(attr_layout)
        bottom_layout.add_widget(middle_layout)

        # Right area: Output
        right_layout = BoxLayout(orientation="vertical", size_hint_x=0.3)
        right_layout.add_widget(Label(text="计算结果", font_name=DEFAULT_FONT))
        self.output_label = Label(text=self.output_text, font_name=DEFAULT_FONT)
        right_layout.add_widget(self.output_label)
        bottom_layout.add_widget(right_layout)

        main_layout.add_widget(bottom_layout)

        self.update_form()
        self.calculate_equivalent_damage()

        return main_layout

    def on_faction_select(self, instance, value):
        self.calculate_equivalent_damage()

    def add_weapon(self, instance):
        new_weapon = WeaponData(名称=f"新武器 {len(self.weapon_list) + 1}")
        self.weapon_list.append(new_weapon)
        self.weapon_recycleview.viewclass = "Button"
        self.weapon_recycleview.data = [
            {"text": x.名称, "font_name": DEFAULT_FONT} for x in self.weapon_list
        ]
        self.current_weapon = new_weapon
        self.update_form()
        self.calculate_equivalent_damage()

    def on_weapon_select(self, instance, touch):
        # Simple selection logic for RecycleView
        if instance.collide_point(*touch.pos):
            for index, item in enumerate(self.weapon_recycleview.data):
                # Check if the touch is within the bounds of a list item
                if (
                    self.weapon_recycleview.children
                    and self.weapon_recycleview.children[0].children
                ):
                    list_item_widgets = self.weapon_recycleview.children[0].children
                    # RecycleView items are added from bottom up, so reverse index
                    widget_index = len(list_item_widgets) - 1 - index
                    if 0 <= widget_index < len(list_item_widgets):
                        if list_item_widgets[widget_index].collide_point(*touch.pos):
                            self.current_weapon = self.weapon_list[index]
                            self.update_form()
                            self.calculate_equivalent_damage()
                            break

    def on_attribute_change(self, instance, value):
        # Update current weapon data based on form input
        # Find which attribute input triggered the change
        chinese_attr = None
        for key, input_widget in self.attribute_inputs.items():
            if input_widget == instance:
                chinese_attr = key
                break

        if chinese_attr:
            try:
                setattr(
                    self.current_weapon,
                    chinese_attr,
                    float(value) if value else 0,
                )
            except ValueError:
                pass  # Handle non-numeric input if necessary

        self.calculate_equivalent_damage()

    def update_form(self):
        # Update form inputs based on current weapon data
        if self.current_weapon:
            for chinese_attr, input_widget in self.attribute_inputs.items():
                input_widget.text = str(getattr(self.current_weapon, chinese_attr))

    def calculate_equivalent_damage(self):
        # Placeholder for calculation logic
        if self.current_weapon:
            faction = (
                self.faction_spinner.text
                if self.faction_spinner.text != "选择门派"
                else "未选择门派"
            )
            output = f"门派: {faction}\n"
            output += f"武器: {self.current_weapon.名称}\n"
            output += "属性:\n"
            output += f"  命中: {self.current_weapon.命中}\n"
            output += f"  伤害: {self.current_weapon.伤害}\n"
            output += f"  体质: {self.current_weapon.体质}\n"
            output += f"  魔力: {self.current_weapon.魔力}\n"
            output += f"  力量: {self.current_weapon.力量}\n"
            output += f"  耐力: {self.current_weapon.耐力}\n"
            output += f"  敏捷: {self.current_weapon.敏捷}\n"
            output += "\n等效伤害: (待实现)"
            self.output_text = output
            self.output_label.text = self.output_text


if __name__ == "__main__":
    CalculatorApp().run()
