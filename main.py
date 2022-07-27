from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem, TwoLineIconListItem, IconLeftWidget, ThreeLineIconListItem

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

import requests
from functools import partial

# helper_text: "test"
# helper_text_mode: "on_focus"

login_url = "https://contaxmanagerapp.herokuapp.com/dj-rest-auth/login/"
register_url = "https://contaxmanagerapp.herokuapp.com/dj-rest-auth/registration/"
contacts_url = "https://contaxmanagerapp.herokuapp.com/api/contacts/"
details_url = "https://contaxmanagerapp.herokuapp.com/api/contacts/"

loader = """
<LoginScreen>:
    name: 'login'
    MDTextField:
        id: username
        hint_text: "Username"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.65}
        multiline: False
    MDTextField:
        id: password
        hint_text: "Password"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.55}
        multiline: False
    MDRectangleFlatButton:
        text: "Login"
        font_size: '18sp'
        pos_hint: {'center_x':0.4, 'center_y':0.45}
        on_release: app.login(username.text, password.text)
    MDRectangleFlatButton:
        text: "Register"
        font_size: '18sp'
        pos_hint: {'center_x':0.6, 'center_y':0.45}
        on_release: app.register_screen()
<RegisterScreen>:
    name: 'register'
    MDTextField:
        id: username
        hint_text: "Username"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.75}
        multiline: False
    MDTextField:
        id: email
        hint_text: "Email"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.65}
        multiline: False
    MDTextField:
        id: password
        hint_text: "Password"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.55}
        multiline: False
    MDTextField:
        id: password2
        hint_text: "Confirm Password"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.45}
        multiline: False
    MDRectangleFlatButton:
        text: "Back"
        font_size: '18sp'
        pos_hint: {'center_x':0.4, 'center_y':0.35}
        on_release: app.back_to_login()
    MDRectangleFlatButton:
        text: "Register"
        font_size: '18sp'
        pos_hint: {'center_x':0.6, 'center_y':0.35}
        on_release: app.register(username.text, email.text, password.text, password2.text)
<ContactsScreen>:
    name: 'list'
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            size_hint: 1, 0.1
            text: 'My Contacts'
            halign: 'center'
            font_style: 'H3'
            theme_text_color: 'Custom'
            text_color: 0.16, 0.77, 0.96, 1
        ScrollView:
            MDList:
                id: contacts
<DetailsScreen>:
    name: 'details'
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            id: name
            size_hint: 1, 0.1
            text: ''
            halign: 'center'
            font_style: 'H3'
            theme_text_color: 'Custom'
            text_color: 0.16, 0.77, 0.96, 1
        MDLabel:
            id: description
            size_hint: 0.6, 0.2
            pos_hint: {'center_x': 0.5}
            text:''
            halign: 'center'
            font_style: 'Body1'
        ScrollView:
            MDList:
                id: details
"""

Builder.load_string(loader)

class LoginScreen(Screen):
    pass

class ContactsScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class DetailsScreen(Screen):
    pass

class ContaXApp(MDApp):

    def build(self):
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(ContactsScreen(name='list'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(DetailsScreen(name='details'))
        
        return self.sm

    def login(self, uname, pwd):
        self.sm.get_screen('login').ids.username.text = ""
        self.sm.get_screen('login').ids.password.text = ""

        if uname == "" or pwd == "":
            check_string = 'Both Fields are required!'
            close_button = MDFlatButton(text="Close", on_release=self.close_login_dialog)
        else:
            login_data = {
                "username": uname,
                "password": pwd
            }
            response = requests.post(login_url, data=login_data)

            resp = response.json()
            if 'key' in resp:
                check_string = "Successfully Logged In!"
                close_button = MDFlatButton(text="Close", on_release=self.logged_in)
                self.headers = {
                    "Authorization": f"Token {resp['key']}"
                }
            else:
                check_string = "Invalid credentials!"
                close_button = MDFlatButton(text="Close", on_release=self.close_login_dialog)
            
        self.login_dialog = MDDialog(title ="Login", text=check_string, buttons=[close_button])
        self.login_dialog.open()

    def close_login_dialog(self, obj):
        self.login_dialog.dismiss()

    def logged_in(self, obj):
        try:
            self.login_dialog.dismiss()
        except:
            pass
        try:
            self.register_dialog.dismiss()
        except:
            pass

        self.root.current = 'list'
        
        response = requests.get(contacts_url, headers=self.headers)
        resp = response.json()
        i = 0
        for ct in resp:
            i += 1
            if i%2:
                bg = (0.06,0.06,0.06,1)
            else:
                bg = (0.05,0.05,0.05,1)
            self.sm.get_screen('list').ids.contacts.add_widget(
                TwoLineListItem(text=ct['name'], secondary_text=ct['description'].split('\n')[0],
                font_style='H6', secondary_font_style='Body1',
                bg_color=bg, secondary_theme_text_color = 'Custom', 
                secondary_text_color = (0, 0.5, 0.7, 1),
                on_release = partial(self.contact_details, ct['id'])
                )
            )

    def register_screen(self):
        self.root.current = 'register'
    
    def back_to_login(self):
        self.root.current = 'login'

    def register(self, uname, email, pwd, pwd2):
        # print(uname, email, pwd, pwd2)
        self.sm.get_screen('register').ids.username.text = ""
        self.sm.get_screen('register').ids.email.text = ""
        self.sm.get_screen('register').ids.password.text = ""
        self.sm.get_screen('register').ids.password2.text = ""

        if uname == "" or pwd == "" or pwd2 == "":
            check_string = 'Required Fields are missing!'
            close_button = MDFlatButton(text="Close", on_release=self.close_register_dialog)
        else:
            register_data = {
                "username": uname,
                "email": email,
                "password1": pwd,
                "password2": pwd2
            }
            response = requests.post(register_url, data=register_data)

            resp = response.json()
            # print(resp)
            if 'key' in resp:
                check_string = "Successfully Registered!"
                close_button = MDFlatButton(text="Close", on_release=self.logged_in)
                self.headers = {
                    "Authorization": f"Token {resp['key']}"
                }
            else:
                check_string = "Invalid Data!"
                close_button = MDFlatButton(text="Close", on_release=self.close_register_dialog)
            
        self.register_dialog = MDDialog(title ="Register", text=check_string, buttons=[close_button])
        self.register_dialog.open()

        
    def close_register_dialog(self, obj):
        self.register_dialog.dismiss()

    def registered(self, obj):
        self.register_dialog.dismiss()
        self.root.current = 'list'


    def contact_details(self, id, ele):
        self.root.current = 'details'
        response = requests.get(f"{details_url}{id}/",headers=self.headers)
        resp = response.json()
        self.sm.get_screen('details').ids.name.text = resp['name']
        self.sm.get_screen('details').ids.description.text = resp['description']

        if resp['mobile1']:
            lst_item = TwoLineIconListItem(
                    text = "Mobile",
                    secondary_text = resp['mobile1']
                )
            lst_item.add_widget(IconLeftWidget(icon="phone"))
            self.sm.get_screen('details').ids.details.add_widget(lst_item)

        if resp['mobile2']:
            lst_item = TwoLineIconListItem(
                    text = "Mobile",
                    secondary_text = resp['mobile2']
                )
            lst_item.add_widget(IconLeftWidget(icon="phone"))
            self.sm.get_screen('details').ids.details.add_widget(lst_item)

        if resp['email']:
            lst_item = TwoLineIconListItem(
                    text = "Email",
                    secondary_text = resp['email']
                )
            lst_item.add_widget(IconLeftWidget(icon="email"))
            self.sm.get_screen('details').ids.details.add_widget(lst_item)

        if resp['address']:
            lines = resp['address'].split('\n')
            no_of_lines = len(lines)
            # print(no_of_lines)
            lst_item = ThreeLineIconListItem(
                    text = "Address",
                    secondary_text = "".join(lines[:no_of_lines//2]),
                    tertiary_text = "".join(lines[no_of_lines//2:])
                )
            lst_item.add_widget(IconLeftWidget(icon="home"))
            self.sm.get_screen('details').ids.details.add_widget(lst_item)

ContaXApp().run()