from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

import requests

# helper_text: "test"
# helper_text_mode: "on_focus"

login_url = "https://contaxmanagerapp.herokuapp.com/dj-rest-auth/login/"

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
    MDFloatingActionButton:
        icon: "location-enter"
        pos_hint: {'center_x': 0.5, 'center_y':0.45}
        on_release: app.login(username.text, password.text)
<ContactsScreen>:
    name: 'list'
    MDLabel:
        text: "CONTACTS LIST"
"""

Builder.load_string(loader)

class LoginScreen(Screen):
    pass

class ContactsScreen(Screen):
    pass

class ContaXApp(MDApp):

    def build(self):
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(ContactsScreen(name='list'))
        
        return self.sm

    def login(self, uname, pwd):
        self.sm.get_screen('login').ids.username.text = ""
        self.sm.get_screen('login').ids.password.text = ""

        if uname == "" or pwd == "":
            check_string = 'Both Fields are required!'
            close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
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
            else:
                check_string = "Invalid credentials!"
                close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
            
        self.login_dialog = MDDialog(title ="Login", text=check_string, buttons=[close_button])
        self.login_dialog.open()

    def close_dialog(self, obj):
        self.login_dialog.dismiss()

    def logged_in(self, obj):
        self.login_dialog.dismiss()
        self.root.current = 'list'

ContaXApp().run()