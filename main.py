__version__ = "10.0.0"

import os, sqlite3, hashlib, secrets
from datetime import datetime, timedelta

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, OneLineIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.divider import MDDivider
from kivymd.uix.selectioncontrol import MDCheckbox

# ============================================================
#         آپ انبار (Up Anbar) - نسخه 10.0
#         سازنده: مهدی طریری
#         تلگرام: @mahdi_tar
#         گیت‌هاب: github.com/mahditariri-c
# ============================================================

FONT = "Roboto"
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
try:
    ui_regular = os.path.join(FONT_DIR, "NotoSansArabicUI-Regular.ttf")
    arabic_regular = os.path.join(FONT_DIR, "NotoSansArabic-Regular.ttf")
    if os.path.exists(ui_regular):
        LabelBase.register(name="NotoArabicUI", fn_regular=ui_regular)
        FONT = "NotoArabicUI"
    elif os.path.exists(arabic_regular):
        LabelBase.register(name="NotoArabic", fn_regular=arabic_regular)
        FONT = "NotoArabic"
    else:
        vazir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Vazir.ttf")
        if os.path.exists(vazir):
            LabelBase.register(name="Vazir", fn_regular=vazir)
            FONT = "Vazir"
except Exception as e:
    print("Font error:", e)

KV = """
<CustomCard@MDCard>:
    radius: dp(16)
    elevation: 4
    padding: dp(12)

<StatCard@MDCard>:
    radius: dp(16)
    elevation: 5
    padding: dp(10)
    orientation: "vertical"
    spacing: dp(4)
    size_hint_y: None
    height: dp(110)
    md_bg_color: app.theme_cls.primary_color

<MenuButton@MDRaisedButton>:
    size_hint_y: None
    height: dp(50)
    radius: dp(12)
    font_name: app.font_name

<NavItem@OneLineIconListItem>:
    on_release: app.on_nav_press(self.text)

<LockScreen@MDScreen>:
    name: "lock"
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(30)
        spacing: dp(18)
        Widget:
        MDIcon:
            icon: "warehouse"
            icon_size: dp(90)
            halign: "center"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
        MDLabel:
            text: app.t("app_title")
            font_style: "H4"
            bold: True
            halign: "center"
            font_name: app.font_name
        MDLabel:
            text: app.t("password")
            halign: "center"
            theme_text_color: "Hint"
            font_name: app.font_name
        MDTextField:
            id: password_field
            hint_text: "رمز عبور"
            password: True
            mode: "rectangle"
            size_hint_x: .9
            pos_hint: {"center_x": .5}
            font_name: app.font_name
        MenuButton:
            text: app.t("login")
            size_hint_x: .9
            pos_hint: {"center_x": .5}
            on_press: app.check_password(password_field.text)
        MDLabel:
            text: "سازنده: مهدی طریری | @mahdi_tar"
            halign: "center"
            font_style: "Caption"
            theme_text_color: "Hint"
            font_name: app.font_name
        Widget:

<SetupScreen@MDScreen>:
    name: "setup"
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(30)
        spacing: dp(16)
        Widget:
        MDIcon:
            icon: "shield-check"
            icon_size: dp(80)
            halign: "center"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
        MDLabel:
            text: app.t("app_title")
            font_style: "H4"
            bold: True
            halign: "center"
            font_name: app.font_name
        MDLabel:
            text: app.t("create_password")
            halign: "center"
            font_name: app.font_name
        MDTextField:
            id: setup_password
            hint_text: app.t("new_password")
            password: True
            mode: "rectangle"
            font_name: app.font_name
        MDTextField:
            id: setup_confirm
            hint_text: app.t("confirm_password")
            password: True
            mode: "rectangle"
            font_name: app.font_name
        MenuButton:
            text: app.t("save")
            on_press: app.create_initial_password()
        MDLabel:
            text: "سازنده: مهدی طریری | @mahdi_tar"
            halign: "center"
            font_style: "Caption"
            theme_text_color: "Hint"
            font_name: app.font_name
        Widget:

<HomeScreen@MDScreen>:
    name: "home"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "آپ انبار"
            right_action_items: [["menu", lambda x: app.open_nav()]]
            md_bg_color: app.theme_cls.primary_color
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(12)
                padding: dp(12)
                size_hint_y: None
                height: self.minimum_height
                CustomCard:
                    size_hint_y: None
                    height: dp(125)
                    MDBoxLayout:
                        orientation: "vertical"
                        MDLabel:
                            text: app.t("welcome")
                            font_style: "H5"
                            bold: True
                            font_name: app.font_name
                        MDLabel:
                            text: app.t("inventory_system")
                            theme_text_color: "Hint"
                            font_name: app.font_name
                        MDLabel:
                            text: app.get_today()
                            theme_text_color: "Hint"
                            font_name: app.font_name
                GridLayout:
                    cols: 2
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(230)
                    StatCard:
                        MDIcon:
                            icon: "package-variant"
                            icon_size: dp(35)
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                        MDLabel:
                            id: home_total
                            text: "0"
                            font_style: "H4"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                        MDLabel:
                            text: "نوع کالا"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                    StatCard:
                        md_bg_color: app.theme_cls.accent_color
                        MDIcon:
                            icon: "cash-multiple"
                            icon_size: dp(35)
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                        MDLabel:
                            id: home_value
                            text: "0"
                            font_style: "H4"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                        MDLabel:
                            text: "ارزش فروش موجودی"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(55)
                    spacing: dp(10)
                    MenuButton:
                        text: "افزودن کالا"
                        size_hint_x: .5
                        on_press: app.clear_form(); app.change_screen("add")
                    MenuButton:
                        text: "لیست کالاها"
                        size_hint_x: .5
                        on_press: app.load_products(); app.change_screen("products")
                MDLabel:
                    id: alert_label
                    text: ""
                    size_hint_y: None
                    height: dp(25) if self.text else 0
                    theme_text_color: "Error"
                    font_name: app.font_name
                MDLabel:
                    text: "آخرین کالاها"
                    font_style: "H6"
                    bold: True
                    size_hint_y: None
                    height: dp(30)
                    font_name: app.font_name
                CustomCard:
                    size_hint_y: None
                    height: dp(200)
                    ScrollView:
                        MDList:
                            id: recent_list

<ProductsScreen@MDScreen>:
    name: "products"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "مدیریت کالا"
            right_action_items: [["menu", lambda x: app.open_nav()]]
            md_bg_color: app.theme_cls.primary_color
        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(8)
            spacing: dp(8)
            MDTextField:
                id: search_field
                hint_text: "جستجو..."
                mode: "rectangle"
                size_hint_x: .78
                on_text: app.on_search_text(self.text)
                font_name: app.font_name
            MDIconButton:
                icon: "magnify"
                on_press: app.search_products(search_field.text)
        MDLabel:
            id: product_count
            text: "0 کالا"
            size_hint_y: None
            height: dp(24)
            padding_x: dp(12)
            theme_text_color: "Hint"
            font_name: app.font_name
        ScrollView:
            MDList:
                id: product_list

<AddScreen@MDScreen>:
    name: "add"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            id: add_toolbar
            title: "ثبت کالای جدید"
            right_action_items: [["menu", lambda x: app.open_nav()]]
            md_bg_color: app.theme_cls.primary_color
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(10)
                padding: dp(15)
                size_hint_y: None
                height: self.minimum_height
                CustomCard:
                    size_hint_y: None
                    height: dp(720)
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(10)
                        padding: dp(15)
                        MDLabel:
                            text: "اطلاعات کالا"
                            font_style: "H6"
                            bold: True
                            font_name: app.font_name
                        MDTextField:
                            id: name_field
                            hint_text: "نام کالا *"
                            mode: "rectangle"
                            font_name: app.font_name
                        MDTextField:
                            id: barcode_field
                            hint_text: "بارکد"
                            mode: "rectangle"
                            font_name: app.font_name
                        MDTextField:
                            id: category_field
                            hint_text: "دسته‌بندی"
                            mode: "rectangle"
                            font_name: app.font_name
                        MDTextField:
                            id: price_field
                            hint_text: "قیمت فروش (تومان)"
                            input_filter: "float"
                            mode: "rectangle"
                            font_name: app.font_name
                        MDTextField:
                            id: purchase_field
                            hint_text: "قیمت خرید (تومان)"
                            input_filter: "float"
                            mode: "rectangle"
                            font_name: app.font_name
                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(65)
                            spacing: dp(8)
                            MDTextField:
                                id: quantity_field
                                hint_text: "تعداد"
                                text: "1"
                                input_filter: "int"
                                mode: "rectangle"
                                font_name: app.font_name
                            MDTextField:
                                id: min_quantity_field
                                hint_text: "حداقل موجودی"
                                text: "5"
                                input_filter: "int"
                                mode: "rectangle"
                                font_name: app.font_name
                        MDTextField:
                            id: date_field
                            hint_text: "تاریخ ثبت"
                            text: app.get_today()
                            mode: "rectangle"
                            font_name: app.font_name
                        MDTextField:
                            id: desc_field
                            hint_text: "توضیحات"
                            multiline: True
                            size_hint_y: None
                            height: dp(80)
                            mode: "rectangle"
                            font_name: app.font_name
                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(55)
                            spacing: dp(10)
                            MenuButton:
                                id: submit_btn
                                text: "ثبت کالا"
                                size_hint_x: .6
                                on_press: app.submit_product()
                            MenuButton:
                                text: "انصراف"
                                size_hint_x: .4
                                on_press: app.clear_form(); app.change_screen("products")

<SellScreen@MDScreen>:
    name: "sell"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "ثبت فروش"
            right_action_items: [["menu", lambda x: app.open_nav()]]
            md_bg_color: app.theme_cls.primary_color
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(12)
                padding: dp(15)
                size_hint_y: None
                height: self.minimum_height
                CustomCard:
                    size_hint_y: None
                    height: dp(620)
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(12)
                        padding: dp(15)
                        MDLabel:
                            text: "اطلاعات فروش"
                            font_style: "H6"
                            bold: True
                            font_name: app.font_name
                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(65)
                            spacing: dp(8)
                            MDTextField:
                                id: sell_product_field
                                hint_text: "کد، بارکد یا نام کالا"
                                mode: "rectangle"
                                font_name: app.font_name
                            MDIconButton:
                                icon: "magnify"
                                on_press: app.find_product_for_sale()
                        MDLabel:
                            id: sell_product_info
                            text: "کالایی انتخاب نشده"
                            theme_text_color: "Hint"
                            font_name: app.font_name
                        MDTextField:
                            id: sell_qty_field
                            hint_text: "تعداد فروش"
                            text: "1"
                            input_filter: "int"
                            mode: "rectangle"
                            on_text: app.update_sale_total_ui()
                            font_name: app.font_name
                        MDTextField:
                            id: sell_price_field
                            hint_text: "قیمت واحد"
                            input_filter: "float"
                            mode: "rectangle"
                            on_text: app.update_sale_total_ui()
                            font_name: app.font_name
                        MDTextField:
                            id: sell_customer_field
                            hint_text: "نام مشتری (اختیاری)"
                            mode: "rectangle"
                            font_name: app.font_name
                        MDLabel:
                            id: sell_total_label
                            text: "مبلغ کل: 0 تومان"
                            font_style: "H6"
                            bold: True
                            font_name: app.font_name
                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(55)
                            spacing: dp(10)
                            MenuButton:
                                text: app.t("sell")
                                size_hint_x: .6
                                on_press: app.submit_sale()
                            MenuButton:
                                text: "پاک کردن"
                                size_hint_x: .4
                                on_press: app.clear_sale_form()

<SalesHistoryScreen@MDScreen>:
    name: "sales_history"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "تاریخچه فروش"
            right_action_items: [["menu", lambda x: app.open_nav()]]
            md_bg_color: app.theme_cls.primary_color
        MDLabel:
            id: sales_count
            text: "0 فروش"
            size_hint_y: None
            height: dp(25)
            padding_x: dp(12)
            theme_text_color: "Hint"
            font_name: app.font_name
        ScrollView:
            MDList:
                id: sales_list

<StatsScreen@MDScreen>:
    name: "stats"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "آمار و تحلیل"
            right_action_items: [["menu", lambda x: app.open_nav()]]
            md_bg_color: app.theme_cls.primary_color
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(10)
                padding: dp(12)
                size_hint_y: None
                height: self.minimum_height
                GridLayout:
                    cols: 2
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(230)
                    StatCard:
                        MDLabel:
                            id: stat_total
                            text: "0"
                            font_style: "H3"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                        MDLabel:
                            text: "نوع کالا"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                    StatCard:
                        md_bg_color: app.theme_cls.accent_color
                        MDLabel:
                            id: stat_value
                            text: "0"
                            font_style: "H4"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                        MDLabel:
                            text: "ارزش فروش موجودی"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                GridLayout:
                    cols: 2
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(230)
                    StatCard:
                        md_bg_color: [.2,.7,.3,1]
                        MDLabel:
                            id: stat_qty
                            text: "0"
                            font_style: "H3"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                        MDLabel:
                            text: "مجموع موجودی"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                    StatCard:
                        md_bg_color: [.9,.4,.1,1]
                        MDLabel:
                            id: stat_low
                            text: "0"
                            font_style: "H3"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                        MDLabel:
                            text: "موجودی کم"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: [1,1,1,1]
                CustomCard:
                    size_hint_y: None
                    height: dp(280)
                    MDLabel:
                        id: detail_label
                        text: "در حال بارگذاری..."
                        font_name: app.font_name
                MenuButton:
                    text: app.t("export_excel")
                    on_press: app.export_excel()

<ChartsScreen@MDScreen>:
    name: "charts"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "نمودار فروش"
            right_action_items: [["menu", lambda x: app.open_nav()]]
            md_bg_color: app.theme_cls.primary_color
        MDBoxLayout:
            id: chart_container
            orientation: "vertical"
            padding: dp(10)
        MDLabel:
            text: "فروش روزانه ۷ روز اخیر"
            halign: "center"
            size_hint_y: None
            height: dp(30)
            font_name: app.font_name

<SettingsScreen@MDScreen>:
    name: "settings"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "تنظیمات"
            right_action_items: [["menu", lambda x: app.open_nav()]]
            md_bg_color: app.theme_cls.primary_color
        ScrollView:
            MDList:
                OneLineIconListItem:
                    text: app.t("language")
                    on_press: app.show_language_dialog()
                    IconLeftWidget:
                        icon: "translate"
                OneLineIconListItem:
                    text: app.t("change_theme")
                    on_press: app.toggle_theme()
                    IconLeftWidget:
                        icon: "brightness-4"
                OneLineIconListItem:
                    text: app.t("change_password")
                    on_press: app.show_change_password_dialog()
                    IconLeftWidget:
                        icon: "lock-reset"
                OneLineIconListItem:
                    text: app.t("export_excel")
                    on_press: app.export_excel()
                    IconLeftWidget:
                        icon: "microsoft-excel"
                OneLineIconListItem:
                    text: app.t("export_pdf")
                    on_press: app.export_pdf()
                    IconLeftWidget:
                        icon: "file-pdf-box"
                OneLineIconListItem:
                    text: app.t("backup")
                    on_press: app.backup_database()
                    IconLeftWidget:
                        icon: "database-export"
                OneLineIconListItem:
                    text: app.t("about")
                    on_press: app.change_screen("about")
                    IconLeftWidget:
                        icon: "information"

<AboutScreen@MDScreen>:
    name: "about"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "درباره برنامه"
            right_action_items: [["menu", lambda x: app.open_nav()]]
            md_bg_color: app.theme_cls.primary_color
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                MDIcon:
                    icon: "warehouse"
                    icon_size: dp(80)
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                MDLabel:
                    text: "آپ انبار"
                    font_style: "H3"
                    bold: True
                    halign: "center"
                    theme_text_color: "Primary"
                    font_name: app.font_name
                MDLabel:
                    text: "Up Anbar"
                    font_style: "Subtitle1"
                    halign: "center"
                    theme_text_color: "Hint"
                MDLabel:
                    text: "سیستم مدیریت هوشمند انبار و فروشگاه"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Hint"
                    font_name: app.font_name
                MDLabel:
                    text: "نسخه 10.0"
                    font_style: "Body2"
                    halign: "center"
                    theme_text_color: "Hint"
                    font_name: app.font_name
                MDDivider:
                    height: dp(1)
                MDLabel:
                    text: "سازنده و توسعه‌دهنده"
                    font_style: "Subtitle2"
                    bold: True
                    halign: "center"
                    theme_text_color: "Primary"
                    font_name: app.font_name
                MDLabel:
                    text: "مهدی طریری"
                    font_style: "H5"
                    bold: True
                    halign: "center"
                    font_name: app.font_name
                MDLabel:
                    text: "Mahdi Tariri"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Hint"
                MDDivider:
                    height: dp(1)
                MDLabel:
                    text: "راه‌های ارتباطی"
                    font_style: "Subtitle2"
                    bold: True
                    halign: "center"
                    theme_text_color: "Primary"
                    font_name: app.font_name
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    spacing: dp(6)
                    MDIcon:
                        icon: "send"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                    MDLabel:
                        text: "تلگرام: @mahdi_tar"
                        font_style: "Body1"
                        font_name: app.font_name
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    spacing: dp(6)
                    MDIcon:
                        icon: "github"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primary_color
                    MDLabel:
                        text: "github.com/mahditariri-c"
                        font_style: "Body1"
                        font_name: app.font_name
                MDDivider:
                    height: dp(1)
                MDLabel:
                    text: "قابلیت‌های برنامه"
                    font_style: "Subtitle2"
                    bold: True
                    halign: "center"
                    theme_text_color: "Primary"
                    font_name: app.font_name
                MDLabel:
                    text: "▪ مدیریت کامل کالاها\\n▪ ثبت فروش و محاسبه سود\\n▪ تاریخچه فروش\\n▪ آمار و تحلیل دقیق\\n▪ نمودار فروش ۷ روزه\\n▪ تحویل و بازتحویل به همکار\\n▪ خروجی Excel و PDF\\n▪ پشتیبان‌گیری خودکار\\n▪ قفل با رمز عبور\\n▪ پشتیبانی از ۳ زبان (فارسی/انگلیسی/عربی)"
                    font_style: "Body2"
                    halign: "right"
                    theme_text_color: "Hint"
                    font_name: app.font_name
                MDDivider:
                    height: dp(1)
                MDLabel:
                    text: "© 2024 - تمامی حقوق محفوظ است"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Hint"
                    font_name: app.font_name

<HandoverScreen@MDScreen>:
    name: "handover"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            id: handover_toolbar
            title: "تحویل / بازتحویل"
            right_action_items: [["menu", lambda x: app.open_nav()]]
            md_bg_color: app.theme_cls.primary_color
        ScrollView:
            do_scroll_x: False
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(10)
                padding: dp(14)
                size_hint_y: None
                height: self.minimum_height
                CustomCard:
                    size_hint_y: None
                    height: dp(570)
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(10)
                        padding: dp(12)
                        MDLabel:
                            id: action_label
                            text: app.t("handover")
                            font_style: "H6"
                            bold: True
                            halign: "center"
                            font_name: app.font_name
                        MDLabel:
                            id: live_clock
                            text: app.get_device_datetime()
                            halign: "center"
                            theme_text_color: "Hint"
                            font_name: app.font_name
                        MDTextField:
                            id: action_field
                            text: "handover"
                            opacity: 0
                            disabled: True
                            size_hint_y: None
                            height: 0
                        MDTextField:
                            id: product_field
                            hint_text: "کد، بارکد یا نام کالا *"
                            mode: "rectangle"
                            font_name: app.font_name
                        MDTextField:
                            id: colleague_field
                            hint_text: "نام همکار *"
                            mode: "rectangle"
                            font_name: app.font_name
                        MDTextField:
                            id: handover_qty
                            hint_text: "تعداد *"
                            text: "1"
                            input_filter: "int"
                            mode: "rectangle"
                            font_name: app.font_name
                        MDTextField:
                            id: event_time
                            hint_text: "تاریخ و ساعت"
                            text: app.get_device_datetime()
                            mode: "rectangle"
                            readonly: True
                            font_name: app.font_name
                        MDTextField:
                            id: handover_note
                            hint_text: "توضیحات"
                            mode: "rectangle"
                            multiline: True
                            size_hint_y: None
                            height: dp(80)
                            font_name: app.font_name
                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(52)
                            spacing: dp(8)
                            MenuButton:
                                text: "ثبت عملیات"
                                size_hint_x: .5
                                md_bg_color: app.theme_cls.primary_color
                                on_press: app.submit_handover()
                            MenuButton:
                                text: "به‌روزرسانی تاریخچه"
                                size_hint_x: .5
                                md_bg_color: app.theme_cls.accent_color
                                on_press: app.show_handover_history()
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(52)
                    spacing: dp(8)
                    MenuButton:
                        text: app.t("export_excel")
                        size_hint_x: .5
                        on_press: app.export_handover_excel()
                    MenuButton:
                        text: app.t("export_pdf")
                        size_hint_x: .5
                        on_press: app.export_handover_pdf()
                CustomCard:
                    size_hint_y: None
                    height: dp(360)
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: dp(10)
                        MDLabel:
                            text: "تاریخچه تحویل و بازتحویل"
                            font_style: "H6"
                            bold: True
                            font_name: app.font_name
                        ScrollView:
                            do_scroll_x: False
                            MDList:
                                id: handover_history

<RootScreen>:
    MDNavigationDrawer:
        id: nav_drawer
        radius: [0, dp(20), dp(20), 0]
        MDBoxLayout:
            orientation: "vertical"
            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: dp(220)
                padding: dp(10)
                spacing: dp(3)
                MDIconButton:
                    icon: "account-circle"
                    icon_size: dp(70)
                    pos_hint: {"center_x": .5}
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                MDLabel:
                    text: "مهدی طریری"
                    font_style: "H6"
                    bold: True
                    halign: "center"
                    theme_text_color: "Primary"
                    font_name: app.font_name
                MDLabel:
                    text: "سازنده و توسعه‌دهنده"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Hint"
                    font_name: app.font_name
                MDLabel:
                    text: "تلگرام: @mahdi_tar"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Hint"
                    font_name: app.font_name
                MDLabel:
                    text: "github.com/mahditariri-c"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Hint"
                    font_name: app.font_name
                MDDivider:
                    height: dp(1)
            ScrollView:
                MDList:
                    NavItem:
                        text: app.t("home")
                        IconLeftWidget:
                            icon: "home"
                    NavItem:
                        text: app.t("products")
                        IconLeftWidget:
                            icon: "format-list-bulleted"
                    NavItem:
                        text: app.t("add_product")
                        IconLeftWidget:
                            icon: "plus-circle"
                    NavItem:
                        text: app.t("sell")
                        IconLeftWidget:
                            icon: "cart"
                    NavItem:
                        text: app.t("sales_history")
                        IconLeftWidget:
                            icon: "history"
                    NavItem:
                        text: app.t("stats")
                        IconLeftWidget:
                            icon: "chart-bar"
                    NavItem:
                        text: app.t("charts")
                        IconLeftWidget:
                            icon: "chart-line"
                    NavItem:
                        text: app.t("handover")
                        IconLeftWidget:
                            icon: "account-arrow-right"
                    NavItem:
                        text: app.t("return")
                        IconLeftWidget:
                            icon: "account-arrow-left"
                    NavItem:
                        text: app.t("settings")
                        IconLeftWidget:
                            icon: "cog"
                    NavItem:
                        text: app.t("about")
                        IconLeftWidget:
                            icon: "information"
    ScreenManager:
        id: sm
        LockScreen:
        SetupScreen:
        HomeScreen:
        ProductsScreen:
        AddScreen:
        SellScreen:
        SalesHistoryScreen:
        StatsScreen:
        ChartsScreen:
        SettingsScreen:
        AboutScreen:
        HandoverScreen:

RootScreen:
"""


class RootScreen(MDScreen):
    pass


class Database:
    def __init__(self):
        self.path = self._get_path()
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.conn = sqlite3.connect(self.path, check_same_thread=False, timeout=10)
        self.conn.execute("PRAGMA foreign_keys=ON")
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.create_tables()
        self.migrate()

    def _get_path(self):
        try:
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), "up_anbar.db")
        except Exception:
            return os.path.join(os.path.expanduser("~"), ".up_anbar", "up_anbar.db")

    def create_tables(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            barcode TEXT UNIQUE,
            name TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'عمومی',
            price REAL NOT NULL DEFAULT 0,
            purchase_price REAL NOT NULL DEFAULT 0,
            quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity>=0),
            min_quantity INTEGER NOT NULL DEFAULT 5 CHECK(min_quantity>=0),
            date TEXT,
            description TEXT
        );
        CREATE TABLE IF NOT EXISTS sales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity>0),
            unit_price REAL NOT NULL DEFAULT 0,
            purchase_unit_price REAL NOT NULL DEFAULT 0,
            total_price REAL NOT NULL DEFAULT 0,
            profit REAL NOT NULL DEFAULT 0,
            customer TEXT,
            sale_date TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE SET NULL
        );
        CREATE TABLE IF NOT EXISTS settings(
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS handovers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            product_name TEXT NOT NULL,
            colleague TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity>0),
            action TEXT NOT NULL CHECK(action IN ('handover','return')),
            note TEXT,
            event_time TEXT NOT NULL,
            unit_price REAL NOT NULL DEFAULT 0,
            reference TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE SET NULL
        );
        CREATE INDEX IF NOT EXISTS idx_handovers_colleague ON handovers(colleague);
        CREATE INDEX IF NOT EXISTS idx_handovers_product ON handovers(product_id);
        CREATE INDEX IF NOT EXISTS idx_handovers_time ON handovers(event_time);
        CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
        CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);
        """)
        self.conn.commit()

    def migrate(self):
        cols = {r[1] for r in self.conn.execute("PRAGMA table_info(sales)")}
        if "purchase_unit_price" not in cols:
            self.conn.execute("ALTER TABLE sales ADD COLUMN purchase_unit_price REAL NOT NULL DEFAULT 0")
        if "profit" not in cols:
            self.conn.execute("ALTER TABLE sales ADD COLUMN profit REAL NOT NULL DEFAULT 0")
        self.conn.commit()

    def _code(self):
        while True:
            code = "UP-" + datetime.now().strftime("%Y%m%d%H%M%S%f") + "-" + secrets.token_hex(2).upper()
            if not self.conn.execute("SELECT 1 FROM products WHERE code=?", (code,)).fetchone():
                return code

    def add_product(self, d):
        code = self._code()
        self.conn.execute("""INSERT INTO products
        (code,barcode,name,category,price,purchase_price,quantity,min_quantity,date,description)
        VALUES(?,?,?,?,?,?,?,?,?,?)""", (code,) + tuple(d))
        self.conn.commit()
        return code

    def update_product(self, pid, d):
        self.conn.execute("""UPDATE products SET name=?,price=?,purchase_price=?,
        quantity=?,min_quantity=?,date=?,barcode=?,description=?,category=? WHERE id=?""",
        (d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],pid))
        self.conn.commit()

    def all_products(self):
        return self.conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()

    def product(self, pid):
        return self.conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()

    def by_code(self, value):
        value = (value or "").strip()
        if not value:
            return None
        return self.conn.execute(
            "SELECT * FROM products WHERE code=? OR barcode=? LIMIT 1",
            (value,value)).fetchone()

    def search(self, q):
        q=(q or "").strip()
        if not q: return self.all_products()
        x="%"+q+"%"
        return self.conn.execute("""SELECT * FROM products
        WHERE name LIKE ? OR code LIKE ? OR COALESCE(barcode,'') LIKE ? OR category LIKE ?
        ORDER BY id DESC""",(x,x,x,x)).fetchall()

    def delete(self,pid):
        self.conn.execute("DELETE FROM products WHERE id=?",(pid,))
        self.conn.commit()

    def low(self):
        return self.conn.execute(
            "SELECT * FROM products WHERE quantity<=min_quantity").fetchall()

    def stats(self):
        r=self.conn.execute("""SELECT COUNT(*),COALESCE(SUM(quantity),0),
        COALESCE(SUM(price*quantity),0),COALESCE(SUM(purchase_price*quantity),0),
        COALESCE(AVG(price),0),COALESCE(SUM(quantity<=min_quantity),0)
        FROM products""").fetchone()
        return {"total":r[0],"qty":r[1],"sale_value":r[2],
                "purchase_value":r[3],"avg":r[4],"low":r[5]}

    def sale_stats(self):
        r=self.conn.execute("""SELECT COUNT(*),COALESCE(SUM(quantity),0),
        COALESCE(SUM(total_price),0),COALESCE(SUM(profit),0) FROM sales""").fetchone()
        return {"count":r[0],"qty":r[1],"total":r[2],"profit":r[3]}

    def sell(self,pid,qty,price,customer,date):
        with self.conn:
            p=self.product(pid)
            if not p: raise ValueError("کالا یافت نشد")
            if qty<=0: raise ValueError("تعداد باید بیشتر از صفر باشد")
            if price<0: raise ValueError("قیمت نمی‌تواند منفی باشد")
            if qty>p[7]: raise ValueError(f"موجودی کافی نیست: {p[7]}")
            purchase=p[6]
            total=qty*price
            profit=qty*(price-purchase)
            self.conn.execute("""INSERT INTO sales
            (product_id,product_name,quantity,unit_price,purchase_unit_price,total_price,profit,customer,sale_date)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (p[0],p[3],qty,price,purchase,total,profit,customer,date))
            cur=self.conn.execute(
                "UPDATE products SET quantity=quantity-? WHERE id=? AND quantity>=?",
                (qty,pid,qty))
            if cur.rowcount!=1: raise ValueError("موجودی هنگام فروش تغییر کرده است")
            return total,profit

    def sales(self):
        return self.conn.execute("SELECT * FROM sales ORDER BY id DESC").fetchall()

    def update_quantity(self,pid,new_qty):
        if new_qty < 0:
            raise ValueError("موجودی نمی‌تواند منفی باشد")
        cur=self.conn.execute("UPDATE products SET quantity=? WHERE id=?",(new_qty,pid))
        if cur.rowcount != 1:
            raise ValueError("کالا یافت نشد")
        self.conn.commit()

    def add_handover(self,product_id,product_name,colleague,quantity,action,note,event_time,unit_price,reference=""):
        with self.conn:
            self.conn.execute("""INSERT INTO handovers
            (product_id,product_name,colleague,quantity,action,note,event_time,unit_price,reference)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (product_id,product_name,colleague,quantity,action,note,event_time,unit_price,reference))

    def perform_handover(self,product_id,product_name,colleague,quantity,action,note,event_time,unit_price,reference=""):
        with self.conn:
            product=self.product(product_id)
            if not product:
                raise ValueError("کالا یافت نشد")
            if quantity <= 0:
                raise ValueError("تعداد باید بیشتر از صفر باشد")
            if action == "handover":
                cur=self.conn.execute(
                    "UPDATE products SET quantity=quantity-? WHERE id=? AND quantity>=?",
                    (quantity,product_id,quantity))
                if cur.rowcount != 1:
                    raise ValueError(f"موجودی کافی نیست: {product[7]}")
            elif action == "return":
                balance=self.colleague_balance(colleague,product_id)
                if quantity > balance:
                    raise ValueError(f"بازتحویل بیشتر از موجودی نزد همکار است: {balance}")
                self.conn.execute("UPDATE products SET quantity=quantity+? WHERE id=?",(quantity,product_id))
            else:
                raise ValueError("نوع عملیات نامعتبر است")
            self.conn.execute("""INSERT INTO handovers
            (product_id,product_name,colleague,quantity,action,note,event_time,unit_price,reference)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (product_id,product_name,colleague,quantity,action,note,event_time,unit_price,reference))

    def all_handovers(self):
        return self.conn.execute("SELECT * FROM handovers ORDER BY id DESC").fetchall()

    def colleague_balance(self,colleague,product_id):
        row=self.conn.execute("""SELECT COALESCE(SUM(CASE WHEN action='handover' THEN quantity ELSE -quantity END),0)
            FROM handovers WHERE colleague=? AND product_id=?""",(colleague,product_id)).fetchone()
        return int(row[0] or 0)

    def colleague_balances(self):
        return self.conn.execute("""SELECT colleague, product_id, product_name,
            SUM(CASE WHEN action='handover' THEN quantity ELSE -quantity END) AS balance,
            MAX(event_time) AS last_time
            FROM handovers GROUP BY colleague, product_id
            HAVING balance > 0 ORDER BY colleague, product_name""").fetchall()

    def daily(self,days=7):
        result=[]
        for i in range(days-1,-1,-1):
            d=(datetime.now()-timedelta(days=i)).strftime("%Y-%m-%d")
            v=self.conn.execute(
                "SELECT COALESCE(SUM(total_price),0) FROM sales WHERE sale_date=?",(d,)).fetchone()[0]
            result.append((d,v))
        return result

    def get_setting(self,k,default=None):
        r=self.conn.execute("SELECT value FROM settings WHERE key=?",(k,)).fetchone()
        return r[0] if r else default

    def set_setting(self,k,v):
        self.conn.execute(
            "INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)",(k,v))
        self.conn.commit()

    def backup(self,dst):
        os.makedirs(os.path.dirname(dst),exist_ok=True)
        target=sqlite3.connect(dst)
        try:
            self.conn.commit()
            self.conn.backup(target)
        finally:
            target.close()

    def close(self):
        self.conn.close()


class ProductApp(MDApp):
    font_name=FONT
    TRANSLATIONS = {
        "fa": {
            "app_title":"آپ انبار","create_password":"برای شروع یک رمز عبور مدیر بسازید","new_password":"رمز جدید","confirm_password":"تکرار رمز جدید","save":"ذخیره","language":"زبان","change_theme":"تغییر تم","change_password":"تغییر رمز عبور","export_excel":"خروجی Excel","export_pdf":"خروجی PDF","backup":"پشتیبان‌گیری","about":"درباره برنامه","login":"ورود","password":"رمز عبور","welcome":"سلام، خوش آمدید","inventory_system":"سیستم مدیریت انبار و فروشگاه","home":"خانه","products":"مدیریت کالا","add_product":"ثبت کالای جدید","sell":"ثبت فروش","sales_history":"تاریخچه فروش","stats":"آمار و تحلیل","charts":"نمودار فروش","handover":"تحویل به همکار","return":"بازتحویل از همکار","settings":"تنظیمات","handover_title":"تحویل / بازتحویل"
        },
        "en": {
            "app_title":"Up Anbar","create_password":"Create an administrator password to start","new_password":"New password","confirm_password":"Confirm password","save":"Save","language":"Language","change_theme":"Change theme","change_password":"Change password","export_excel":"Export Excel","export_pdf":"Export PDF","backup":"Backup","about":"About","login":"Sign in","password":"Password","welcome":"Hello, welcome","inventory_system":"Inventory & Sales Management","home":"Home","products":"Products","add_product":"Add Product","sell":"New Sale","sales_history":"Sales History","stats":"Statistics & Analysis","charts":"Sales Chart","handover":"Handover to Colleague","return":"Return from Colleague","settings":"Settings","handover_title":"Handover / Return"
        },
        "ar": {
            "app_title":"أب أنبار","create_password":"أنشئ كلمة مرور المدير للبدء","new_password":"كلمة المرور الجديدة","confirm_password":"تأكيد كلمة المرور","save":"حفظ","language":"اللغة","change_theme":"تغيير المظهر","change_password":"تغيير كلمة المرور","export_excel":"تصدير Excel","export_pdf":"تصدير PDF","backup":"نسخ احتياطي","about":"حول التطبيق","login":"دخول","password":"كلمة المرور","welcome":"مرحباً بك","inventory_system":"إدارة المخزون والمبيعات","home":"الرئيسية","products":"المنتجات","add_product":"إضافة منتج","sell":"بيع جديد","sales_history":"سجل المبيعات","stats":"الإحصاءات والتحليل","charts":"مخطط المبيعات","handover":"تسليم للموظف","return":"إرجاع من الموظف","settings":"الإعدادات","handover_title":"التسليم / الإرجاع"
        }
    }
    edit_product_id=None

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style="Light"
        self.theme_cls.primary_palette="Blue"
        self.theme_cls.accent_palette="Teal"
        self.title = "آپ انبار"
        self.db=Database()
        self.selected_sale_product=None
        self.search_event=None
        self.handover_clock_event=None
        self.language=self.db.get_setting("language","fa")

    def build(self):
        self.root=Builder.load_string(KV)
        Clock.schedule_once(lambda dt:self.startup(),.4)
        return self.root

    def on_stop(self):
        if self.handover_clock_event:
            self.handover_clock_event.cancel()
            self.handover_clock_event = None
        self.db.close()

    def t(self,key):
        return self.TRANSLATIONS.get(self.language,self.TRANSLATIONS["fa"]).get(key,key)

    def create_initial_password(self):
        s=self.root.ids.sm.get_screen("setup")
        p=s.ids.setup_password.text
        c=s.ids.setup_confirm.text
        if len(p)<6:
            self.snack("رمز باید حداقل ۶ کاراکتر باشد" if self.language=="fa" else "Password must be at least 6 characters")
            return
        if p!=c:
            self.snack("تکرار رمز صحیح نیست" if self.language=="fa" else "Passwords do not match")
            return
        self.set_password(p)
        self.change_screen("home")
        self.snack("رمز مدیر ساخته شد" if self.language=="fa" else "Administrator password created")

    def show_language_dialog(self):
        dlg=None
        def choose(lang):
            self.language=lang
            self.db.set_setting("language",lang)
            dlg.dismiss()
            self._refresh_static_text()
        box=MDBoxLayout(orientation="vertical",spacing=dp(6),padding=dp(8),size_hint_y=None,height=dp(170))
        for lang,label in (("fa","فارسی"),("en","English"),("ar","العربية")):
            b=MDRaisedButton(text=label,size_hint_y=None,height=dp(45),on_press=lambda x,l=lang:choose(l))
            box.add_widget(b)
        dlg=MDDialog(title="Language / زبان / اللغة",type="custom",content_cls=box,buttons=[MDFlatButton(text="بستن",on_press=lambda x:dlg.dismiss())])
        dlg.open()

    def _refresh_static_text(self):
        """زبان جدید هنگام راه‌اندازی مجدد اعمال می‌شود."""
        if self.language == "fa":
            self.snack("زبان تغییر کرد. لطفاً برنامه را دوباره باز کنید")
        elif self.language == "ar":
            self.snack("تم تغيير اللغة. يرجى إعادة فتح التطبيق")
        else:
            self.snack("Language changed. Please restart the app")

    def get_today(self):
        return datetime.now().strftime("%Y-%m-%d")

    def snack(self,text,color=None):
        try:
            s=Snackbar(text=str(text),duration=2.5)
            if color: s.bg_color=color
            s.open()
        except Exception: print(text)

    def change_screen(self,name):
        self.root.ids.sm.current=name

    def open_nav(self):
        self.root.ids.nav_drawer.set_state("open")

    def close_nav(self):
        self.root.ids.nav_drawer.set_state("close")

    def on_nav_press(self,text):
        self.close_nav()
        routes={
            self.t("home"):("home",None), self.t("products"):("products",self.load_products),
            self.t("add_product"):("add",self.clear_form), self.t("sell"):("sell",None),
            self.t("sales_history"):("sales_history",self.load_sales_history), self.t("stats"):("stats",self.update_stats),
            self.t("charts"):("charts",self.load_chart), self.t("handover"):("handover",lambda:self.open_handover("handover")),
            self.t("return"):("handover",lambda:self.open_handover("return")), self.t("settings"):("settings",None),
            self.t("about"):("about",None)}
        if text in routes:
            screen,fn=routes[text]
            if fn: fn()
            self.change_screen(screen)

    def startup(self):
        if not self.db.get_setting("password_hash"):
            self.change_screen("setup")
        else:
            self.change_screen("lock")
        self.update_stats()
        self.load_products()
        self.load_recent()
        self.low_stock()
        self.start_clock()
        self.show_handover_history()

    def _hash(self,password,salt):
        return hashlib.pbkdf2_hmac(
            "sha256",password.encode("utf-8"),salt,150000).hex()

    def set_password(self,password):
        salt=secrets.token_bytes(16)
        self.db.set_setting("password_salt",salt.hex())
        self.db.set_setting("password_hash",self._hash(password,salt))

    def verify(self,password):
        try:
            salt=bytes.fromhex(self.db.get_setting("password_salt",""))
            saved=self.db.get_setting("password_hash","")
            return secrets.compare_digest(saved,self._hash(password,salt))
        except Exception:
            return False

    def check_password(self,password):
        if self.verify(password):
            self.root.ids.sm.get_screen("lock").ids.password_field.text=""
            self.change_screen("home")
            self.snack("خوش آمدید")
        else:
            self.snack("رمز عبور اشتباه است")

    def show_change_password_dialog(self):
        old=MDTextField(hint_text="رمز فعلی",password=True)
        new=MDTextField(hint_text="رمز جدید",password=True)
        box=MDBoxLayout(orientation="vertical",spacing=dp(10),
                        padding=dp(10),size_hint_y=None,height=dp(120))
        box.add_widget(old); box.add_widget(new)
        dlg=None
        def save(_):
            if not self.verify(old.text):
                self.snack("رمز فعلی اشتباه است"); return
            if len(new.text)<4:
                self.snack("رمز جدید حداقل ۴ کاراکتر باشد"); return
            self.set_password(new.text)
            dlg.dismiss(); self.snack("رمز تغییر کرد")
        dlg=MDDialog(title="تغییر رمز عبور",type="custom",content_cls=box,
                     buttons=[
                         MDFlatButton(text="لغو",on_press=lambda x:dlg.dismiss()),
                         MDRaisedButton(text="ذخیره",on_press=save)])
        dlg.open()

    def read_form(self):
        s=self.root.ids.sm.get_screen("add")
        name=s.ids.name_field.text.strip()
        if not name: raise ValueError("نام کالا را وارد کنید")
        price=float(s.ids.price_field.text or 0)
        purchase=float(s.ids.purchase_field.text or 0)
        qty=int(s.ids.quantity_field.text or 0)
        minimum=int(s.ids.min_quantity_field.text or 0)
        if price<0 or purchase<0 or qty<0 or minimum<0:
            raise ValueError("مقادیر منفی مجاز نیست")
        return (
            name,price,purchase,qty,minimum,
            s.ids.date_field.text.strip() or self.get_today(),
            s.ids.barcode_field.text.strip() or None,
            s.ids.desc_field.text.strip(),
            s.ids.category_field.text.strip() or "عمومی")

    def submit_product(self):
        try:
            d=self.read_form()
            if self.edit_product_id:
                self.db.update_product(self.edit_product_id,d)
                msg="کالا ویرایش شد"
            else:
                msg="کالا ثبت شد: "+self.db.add_product(d)
            self.clear_form()
            self.load_products()
            self.load_recent()
            self.update_stats()
            self.low_stock()
            self.change_screen("products")
            self.snack(msg)
        except sqlite3.IntegrityError:
            self.snack("بارکد تکراری است")
        except Exception as e:
            self.snack(e)

    def clear_form(self):
        s=self.root.ids.sm.get_screen("add")
        for x in ("name_field","barcode_field","category_field","price_field","purchase_field","desc_field"):
            s.ids[x].text=""
        s.ids.quantity_field.text="1"
        s.ids.min_quantity_field.text="5"
        s.ids.date_field.text=self.get_today()
        self.edit_product_id=None
        s.ids.add_toolbar.title="ثبت کالای جدید"
        s.ids.submit_btn.text="ثبت کالا"

    def load_products(self,products=None):
        s=self.root.ids.sm.get_screen("products")
        products=self.db.all_products() if products is None else products
        s.ids.product_list.clear_widgets()
        s.ids.product_count.text=f"{len(products)} کالا"
        if not products:
            s.ids.product_list.add_widget(
                MDLabel(text="کالایی پیدا نشد",halign="center",
                        size_hint_y=None,height=dp(50)))
            return
        for p in products:
            item=ThreeLineAvatarIconListItem(
                text=p[3],
                secondary_text=f"فروش: {p[5]:,.0f} | موجودی: {p[7]} | {p[4]}",
                tertiary_text=f"کد: {p[1]} | تاریخ: {p[9] or '-'}")
            item.bind(on_release=lambda x,pid=p[0]:self.product_dialog(pid))
            s.ids.product_list.add_widget(item)

    def product_dialog(self,pid):
        p=self.db.product(pid)
        if not p:return
        dlg=None
        def edit(_):
            dlg.dismiss(); self.edit_product(pid)
        def delete(_):
            dlg.dismiss(); self.delete_product(pid)
        text=(f"کد: {p[1]}\nبارکد: {p[2] or 'ندارد'}\n"
              f"دسته: {p[4]}\nقیمت فروش: {p[5]:,.0f}\n"
              f"قیمت خرید: {p[6]:,.0f}\nموجودی: {p[7]}\n"
              f"حداقل موجودی: {p[8]}")
        dlg=MDDialog(title=p[3],text=text,buttons=[
            MDFlatButton(text="بستن",on_press=lambda x:dlg.dismiss()),
            MDRaisedButton(text="ویرایش",on_press=edit),
            MDRaisedButton(text="حذف",on_press=delete)])
        dlg.open()

    def edit_product(self,pid):
        p=self.db.product(pid)
        if not p:return
        self.edit_product_id=pid
        s=self.root.ids.sm.get_screen("add")
        s.ids.name_field.text=p[3] or ""
        s.ids.barcode_field.text=p[2] or ""
        s.ids.category_field.text=p[4] or "عمومی"
        s.ids.price_field.text=str(p[5])
        s.ids.purchase_field.text=str(p[6])
        s.ids.quantity_field.text=str(p[7])
        s.ids.min_quantity_field.text=str(p[8])
        s.ids.date_field.text=p[9] or self.get_today()
        s.ids.desc_field.text=p[10] or ""
        s.ids.add_toolbar.title="ویرایش کالا"
        s.ids.submit_btn.text="ذخیره تغییرات"
        self.change_screen("add")

    def delete_product(self,pid):
        dlg=None
        def yes(_):
            self.db.delete(pid)
            dlg.dismiss()
            self.load_products()
            self.load_recent()
            self.update_stats()
            self.low_stock()
            self.snack("کالا حذف شد")
        dlg=MDDialog(title="حذف کالا",
                     text="کالا حذف می‌شود و تاریخچه فروش حفظ خواهد شد.",
                     buttons=[
                         MDFlatButton(text="لغو",on_press=lambda x:dlg.dismiss()),
                         MDRaisedButton(text="حذف",on_press=yes)])
        dlg.open()

    def load_recent(self):
        l=self.root.ids.sm.get_screen("home").ids.recent_list
        l.clear_widgets()
        for p in self.db.all_products()[:5]:
            l.add_widget(ThreeLineAvatarIconListItem(
                text=p[3],
                secondary_text=f"{p[5]:,.0f} تومان | موجودی {p[7]}",
                tertiary_text=p[9] or "-"))

    def on_search_text(self,text):
        if self.search_event:
            self.search_event.cancel()
        if not text.strip():
            self.load_products()
            return
        self.search_event=Clock.schedule_once(
            lambda dt,q=text:self.load_products(self.db.search(q)),.35)

    def search_products(self,q):
        self.load_products(self.db.search(q))

    def find_product_for_sale(self):
        s=self.root.ids.sm.get_screen("sell")
        q=s.ids.sell_product_field.text.strip()
        p=self.db.by_code(q)
        if not p:
            result=self.db.search(q)
            p=result[0] if result else None
        if not p:
            self.selected_sale_product=None
            s.ids.sell_product_info.text="کالا یافت نشد"
            return
        self.selected_sale_product=p
        s.ids.sell_product_info.text=(
            f"{p[3]} | موجودی {p[7]} | قیمت {p[5]:,.0f}")
        s.ids.sell_price_field.text=str(p[5])
        self.update_sale_total_ui()

    def update_sale_total_ui(self):
        try:
            s=self.root.ids.sm.get_screen("sell")
            total=int(s.ids.sell_qty_field.text or 0)*float(s.ids.sell_price_field.text or 0)
            s.ids.sell_total_label.text=f"مبلغ کل: {total:,.0f} تومان"
        except Exception:
            pass

    def submit_sale(self):
        if not self.selected_sale_product:
            self.snack("اول کالا را انتخاب کنید")
            return
        s=self.root.ids.sm.get_screen("sell")
        try:
            qty=int(s.ids.sell_qty_field.text or 0)
            price=float(s.ids.sell_price_field.text or 0)
            total,profit=self.db.sell(
                self.selected_sale_product[0],qty,price,
                s.ids.sell_customer_field.text.strip() or "مشتری عادی",
                self.get_today())
            self.clear_sale_form()
            self.load_products()
            self.load_recent()
            self.update_stats()
            self.low_stock()
            self.snack(f"فروش ثبت شد | مبلغ {total:,.0f} | سود {profit:,.0f}")
        except Exception as e:
            self.snack(e)

    def clear_sale_form(self):
        s=self.root.ids.sm.get_screen("sell")
        s.ids.sell_product_field.text=""
        s.ids.sell_product_info.text="کالایی انتخاب نشده"
        s.ids.sell_qty_field.text="1"
        s.ids.sell_price_field.text=""
        s.ids.sell_customer_field.text=""
        s.ids.sell_total_label.text="مبلغ کل: 0 تومان"
        self.selected_sale_product=None

    def load_sales_history(self):
        s=self.root.ids.sm.get_screen("sales_history")
        rows=self.db.sales()
        s.ids.sales_list.clear_widgets()
        s.ids.sales_count.text=f"{len(rows)} فروش"
        for x in rows:
            s.ids.sales_list.add_widget(ThreeLineAvatarIconListItem(
                text=x[2],
                secondary_text=f"تعداد {x[3]} | مبلغ {x[6]:,.0f}",
                tertiary_text=f"سود {x[7]:,.0f} | {x[8]} | {x[9]}"))

    def update_stats(self):
        try:
            a=self.db.stats()
            b=self.db.sale_stats()
            h=self.root.ids.sm.get_screen("home")
            s=self.root.ids.sm.get_screen("stats")
            h.ids.home_total.text=str(a["total"])
            h.ids.home_value.text=f'{a["sale_value"]:,.0f}'
            s.ids.stat_total.text=str(a["total"])
            s.ids.stat_value.text=f'{a["sale_value"]:,.0f}'
            s.ids.stat_qty.text=f'{a["qty"]:,}'
            s.ids.stat_low.text=str(a["low"])
            s.ids.detail_label.text=(
                f'نوع کالا: {a["total"]}\n'
                f'مجموع موجودی: {a["qty"]:,}\n'
                f'ارزش خرید موجودی: {a["purchase_value"]:,.0f}\n'
                f'ارزش فروش موجودی: {a["sale_value"]:,.0f}\n'
                f'سود بالقوه موجودی: {a["sale_value"]-a["purchase_value"]:,.0f}\n'
                f'تعداد فروش: {b["count"]}\n'
                f'اقلام فروخته‌شده: {b["qty"]}\n'
                f'درآمد فروش: {b["total"]:,.0f}\n'
                f'سود واقعی فروش: {b["profit"]:,.0f}')
        except Exception as e:
            print("Stats:",e)

    def low_stock(self):
        low=self.db.low()
        a=self.root.ids.sm.get_screen("home").ids.alert_label
        a.text=f"هشدار: {len(low)} کالا با موجودی کم!" if low else ""
        a.height=dp(25) if low else 0

    def load_chart(self):
        c=self.root.ids.sm.get_screen("charts").ids.chart_container
        c.clear_widgets()
        try:
            from kivy_garden.graph import Graph,MeshLinePlot
            d=self.db.daily()
            maximum=max([x[1] for x in d] or [1000],1000)
            g=Graph(xlabel="روز",ylabel="فروش",x_grid=True,y_grid=True,
                    y_grid_label=True,x_grid_label=True,ymin=0,
                    ymax=maximum*1.2,xmin=0,xmax=max(1,len(d)-1),
                    y_ticks_major=max(1,int(maximum/5)))
            p=MeshLinePlot()
            p.points=[(i,x[1]) for i,x in enumerate(d)]
            g.add_plot(p)
            c.add_widget(g)
        except ImportError:
            c.add_widget(MDLabel(text="kivy_garden.graph نصب نیست",halign="center"))

    def export_dir(self):
        try:
            from android.storage import app_storage_path
            d=app_storage_path()
        except Exception:
            d=os.path.join(os.path.expanduser("~"),"UpAnbar")
        os.makedirs(d,exist_ok=True)
        return d

    def export_excel(self):
        try:
            from openpyxl import Workbook
            path=os.path.join(self.export_dir(),f"up_anbar_{datetime.now():%Y%m%d_%H%M%S}.xlsx")
            wb=Workbook()
            ws=wb.active
            ws.title="محصولات"
            ws.sheet_view.rightToLeft = True
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = "A1:J1"
            ws.append(["کد / Code / الرمز","بارکد / Barcode / الباركود","نام / Name / الاسم","دسته / Category / الفئة","قیمت فروش / Sale Price / سعر البيع","قیمت خرید / Purchase Price / سعر الشراء","تعداد / Qty / الكمية","حداقل / Minimum / الحد الأدنى","تاریخ / Date / التاريخ","توضیحات / Notes / ملاحظات"])
            from openpyxl.styles import Font as XLFont, Alignment
            for c in ws[1]:
                c.font = XLFont(bold=True)
                c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            for p in self.db.all_products():
                ws.append([p[1],p[2] or "",p[3],p[4],p[5],p[6],p[7],p[8],p[9] or "",p[10] or ""])
            for row in ws.iter_rows():
                for cell in row:
                    cell.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
            for column in ws.columns:
                max_len=max(len(str(cell.value or "")) for cell in column)
                ws.column_dimensions[column[0].column_letter].width=min(max(max_len+2,12),38)
            wb.save(path)
            self.snack("Excel ذخیره شد")
        except ImportError:
            self.snack("openpyxl نصب نیست")
        except Exception as e:
            self.snack(e)

    def _pdf_text(self,text):
        text=str(text or "")
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            return get_display(arabic_reshaper.reshape(text))
        except Exception:
            return text

    def _pdf_styles(self):
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        font_name="Helvetica"
        candidates=[
            os.path.join(FONT_DIR,"NotoSansArabic-Regular.ttf"),
            os.path.join(FONT_DIR,"NotoSansArabicUI-Regular.ttf"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)),"Vazir.ttf"),
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont("UpAnbarArabic",path))
                    font_name="UpAnbarArabic"
                    break
                except Exception:
                    pass
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name="SmartTitle",parent=styles["Title"],fontName=font_name,fontSize=16,leading=20,alignment=1))
        styles.add(ParagraphStyle(name="SmartBody",parent=styles["BodyText"],fontName=font_name,fontSize=8,leading=10,alignment=1))
        styles.add(ParagraphStyle(name="SmartHead",parent=styles["Heading2"],fontName=font_name,fontSize=11,leading=14,alignment=1))
        return styles,font_name

    def export_pdf(self):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib import colors
            styles,font_name=self._pdf_styles()
            path=os.path.join(self.export_dir(),f"up_anbar_{datetime.now():%Y%m%d_%H%M%S}.pdf")
            data=[[self._pdf_text(x) for x in ["Code / کد / الرمز","Name / نام / الاسم","Category / دسته / الفئة","Price / قیمت / السعر","Qty / تعداد / الكمية"]]]
            for p in self.db.all_products():
                data.append([self._pdf_text(x) for x in [p[1],p[3],p[4],f"{p[5]:,.0f}",str(p[7])]])
            table=Table(data,repeatRows=1)
            table.setStyle(TableStyle([
                ("FONTNAME",(0,0),(-1,-1),font_name),
                ("GRID",(0,0),(-1,-1),.5,colors.black),
                ("BACKGROUND",(0,0),(-1,0),colors.grey),
                ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("FONTSIZE",(0,0),(-1,-1),8),
            ]))
            doc=SimpleDocTemplate(path,pagesize=A4)
            doc.build([Paragraph(self._pdf_text("Up Anbar / آپ انبار"),styles["SmartTitle"]),Spacer(1,10),table])
            self.snack("PDF ذخیره شد")
        except ImportError:
            self.snack("کتابخانه reportlab نصب نیست")
        except Exception as e:
            self.snack(e)

    def backup_database(self):
        try:
            folder=os.path.join(self.export_dir(),"backups")
            os.makedirs(folder,exist_ok=True)
            path=os.path.join(folder,f"backup_{datetime.now():%Y%m%d_%H%M%S}.db")
            self.db.backup(path)
            self.snack("پشتیبان با موفقیت ذخیره شد")
        except Exception as e:
            self.snack(e)

    def get_device_datetime(self):
        return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

    def start_clock(self):
        if self.handover_clock_event is None:
            self.handover_clock_event = Clock.schedule_interval(self._update_clock_labels, 1)

    def _update_clock_labels(self, _dt):
        try:
            screen = self.root.ids.sm.get_screen("handover")
            screen.ids.live_clock.text = self.get_device_datetime()
        except Exception:
            pass

    def open_handover(self, action="handover"):
        self.change_screen("handover")
        screen = self.root.ids.sm.get_screen("handover")
        screen.ids.action_field.text = action
        screen.ids.action_label.text = (
            "تحویل به همکار" if action == "handover" else "بازتحویل از همکار"
        )
        screen.ids.event_time.text = self.get_device_datetime()

    def submit_handover(self):
        try:
            screen = self.root.ids.sm.get_screen("handover")
            query = screen.ids.product_field.text.strip()
            colleague = screen.ids.colleague_field.text.strip()
            qty = int(screen.ids.handover_qty.text or "0")
            action = screen.ids.action_field.text.strip()
            note = screen.ids.handover_note.text.strip()

            if not query or not colleague:
                self.snack("کالا و نام همکار را وارد کنید")
                return
            if qty <= 0:
                self.snack("تعداد باید بیشتر از صفر باشد")
                return

            product = self.db.by_code(query)
            if not product:
                results = self.db.search(query)
                product = results[0] if results else None
            if not product:
                self.snack("کالا یافت نشد")
                return

            event_time = screen.ids.event_time.text.strip() or self.get_device_datetime()
            self.db.perform_handover(
                product[0], product[3], colleague, qty, action, note,
                event_time, product[5]
            )
            self.update_stats()
            self.load_products()
            self.low_stock()

            self.snack(
                "تحویل با موفقیت ثبت شد"
                if action == "handover" else
                "بازتحویل با موفقیت ثبت شد"
            )
            screen.ids.handover_qty.text = "1"
            screen.ids.event_time.text = self.get_device_datetime()
        except Exception as e:
            self.snack(f"خطا: {e}")

    def export_handover_excel(self):
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font as XLFont, Alignment

            wb = Workbook()
            ws = wb.active
            ws.title = "Handover"
            ws.sheet_view.rightToLeft = True
            ws.freeze_panes = "A2"
            headers = [
                "ID / شناسه / المعرّف", "Product / کالا / المنتج",
                "Colleague / همکار / الموظف", "Quantity / تعداد / الكمية",
                "Action / عملیات / العملية", "Note / توضیحات / ملاحظات",
                "Date-Time / تاریخ-زمان / التاريخ-الوقت",
                "Unit Price / قیمت واحد / سعر الوحدة",
                "Reference / مرجع / المرجع"
            ]
            ws.append(headers)
            for c in ws[1]:
                c.font = XLFont(bold=True)
                c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            for row in self.db.all_handovers():
                action = {
                    "handover": "Handover / تحویل / تسليم",
                    "return": "Return / بازتحویل / إرجاع"
                }.get(row[5], row[5])
                values = [
                    row[0], row[2], row[3], row[4], action, row[6],
                    row[7], row[8] if len(row) > 8 else 0,
                    row[9] if len(row) > 9 else ""
                ]
                ws.append(values)

            for column in ws.columns:
                max_len = max(len(str(cell.value or "")) for cell in column)
                ws.column_dimensions[column[0].column_letter].width = min(max_len + 3, 45)

            save_dir = os.getcwd()
            try:
                from android.storage import primary_external_storage_path
                save_dir = primary_external_storage_path()
            except Exception:
                pass
            path = os.path.join(
                save_dir,
                f"handover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            wb.save(path)
            self.snack(f"ذخیره شد: {os.path.basename(path)}")
        except Exception as e:
            self.snack(f"خطا در خروجی: {e}")

    def export_handover_pdf(self):
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib import colors
            rows=self.db.all_handovers()
            balances=self.db.colleague_balances()
            styles,font_name=self._pdf_styles()
            path=os.path.join(self.export_dir(),f"handover_{datetime.now():%Y%m%d_%H%M%S}.pdf")
            doc=SimpleDocTemplate(path,pagesize=landscape(A4))
            story=[Paragraph(self._pdf_text("Handover / تحویل و بازتحویل / التسليم والإرجاع"),styles["SmartTitle"]),Spacer(1,10)]
            data=[[self._pdf_text(x) for x in [
                "ID / شناسه / المعرّف","Product / کالا / المنتج","Colleague / همکار / الموظف",
                "Qty / تعداد / الكمية","Action / عملیات / العملية",
                "Date-Time / تاریخ-زمان / التاريخ-الوقت","Note / توضیحات / ملاحظات"]]]
            for r in rows:
                action="Handover / تحویل / تسليم" if r[5]=="handover" else "Return / بازتحویل / إرجاع"
                data.append([self._pdf_text(x) for x in [r[0],r[2],r[3],r[4],action,r[7],r[6] or ""]])
            table=Table(data,repeatRows=1)
            table.setStyle(TableStyle([
                ("FONTNAME",(0,0),(-1,-1),font_name),
                ("BACKGROUND",(0,0),(-1,0),colors.grey),
                ("TEXTCOLOR",(0,0),(-1,0),colors.whitesmoke),
                ("GRID",(0,0),(-1,-1),.5,colors.black),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("FONTSIZE",(0,0),(-1,-1),7),
            ]))
            story.append(table)
            story.append(Spacer(1,16))
            story.append(Paragraph(self._pdf_text("Outstanding balances / مانده نزد همکار / الرصيد لدى الموظف"),styles["SmartHead"]))
            balance_data=[[self._pdf_text(x) for x in ["Colleague / همکار / الموظف","Product / کالا / المنتج","Balance / مانده / الرصيد","Last Date-Time / آخرین تاریخ-زمان / آخر وقت"]]]
            for b in balances:
                balance_data.append([self._pdf_text(x) for x in [b[0],b[2],b[3],b[4]]])
            if len(balance_data)==1:
                balance_data.append(["-","-","0","-"])
            bt=Table(balance_data,repeatRows=1)
            bt.setStyle(TableStyle([
                ("FONTNAME",(0,0),(-1,-1),font_name),
                ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),
                ("GRID",(0,0),(-1,-1),.5,colors.black),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("FONTSIZE",(0,0),(-1,-1),8),
            ]))
            story.append(bt)
            doc.build(story)
            self.snack(f"PDF ذخیره شد: {os.path.basename(path)}")
        except ImportError:
            self.snack("کتابخانه reportlab یا arabic-reshaper نصب نیست")
        except Exception as e:
            self.snack(f"خطا در PDF: {e}")

    def show_handover_history(self):
        try:
            rows = self.db.all_handovers()
            screen = self.root.ids.sm.get_screen("handover")
            history = screen.ids.handover_history
            history.clear_widgets()
            for r in rows[:100]:
                action = "تحویل" if r[5] == "handover" else "بازتحویل"
                history.add_widget(MDLabel(
                    text=f"{action} | {r[2]} | {r[3]} | {r[4]} عدد | {r[7]}",
                    size_hint_y=None, height=dp(42), font_name=self.font_name
                ))
        except Exception as e:
            print(f"Handover history error: {e}")

    def toggle_theme(self):
        self.theme_cls.theme_style="Dark" if self.theme_cls.theme_style=="Light" else "Light"

    def open_barcode_scanner(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA])
            self.snack("دوربین مجاز شد؛ decoder بارکد باید به‌صورت native به Build اضافه شود")
            return None
        except Exception as e:
            self.snack("اسکن دوربین در این Build فعال نیست؛ بارکد را دستی وارد کنید")
            return None


if __name__ == "__main__":
    ProductApp().run()