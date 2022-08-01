from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem, TwoLineIconListItem, IconLeftWidget, ThreeLineIconListItem

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SwapTransition

import requests
from functools import partial

from kivy.core.window import Window
from kivy.core.clipboard import Clipboard

from kivy.core.window import Window

Window.keyboard_anim_args = {'d':.2, 't':'in_out_expo'}
Window.softinput_mode = "below_target"

Window.size = (462, 1000)

login_url = "https://contaxmanagerapp.herokuapp.com/dj-rest-auth/login/"
register_url = "https://contaxmanagerapp.herokuapp.com/dj-rest-auth/registration/"
contacts_url = "https://contaxmanagerapp.herokuapp.com/api/contacts/"
details_url = "https://contaxmanagerapp.herokuapp.com/api/contacts/"

loader = """
<LoginScreen>:
    name: 'login'
    Image:
        source: 'logo.png'
        pos_hint: {'center_x':0.5, 'center_y':0.77}
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
    MDFloatingActionButton:
        icon: 'arrow-left'
        pos_hint: {'center_y': 0.95}
        theme_text_color: 'Custom'
        md_bg_color: 0.09, 0.08, 0.08, 1
        text_color: 0.16, 0.77, 0.96, 1
        on_release: app.back_to_login()
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
        text: "Register"
        font_size: '18sp'
        pos_hint: {'center_x':0.5, 'center_y':0.35}
        on_release: app.register(username.text, email.text, password.text, password2.text)
<ContactsScreen>:
    name: 'list'
    MDFloatingActionButton:
        icon: 'arrow-left'
        pos_hint: {'center_y': 0.95}
        theme_text_color: 'Custom'
        md_bg_color: 0.09, 0.08, 0.08, 1
        text_color: 0.16, 0.77, 0.96, 1
        on_release: app.list_back()
    MDFloatingActionButton:
        icon: 'account-plus-outline'
        pos_hint: {'center_y': 0.95, 'center_x':0.95}
        theme_text_color: 'Custom'
        md_bg_color: 0.09, 0.08, 0.08, 1
        text_color: 0.16, 0.77, 0.96, 1
        on_release: app.create_contact()
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
    MDFloatingActionButton:
        icon: 'arrow-left'
        pos_hint: {'center_y': 0.95}
        icon_color: '#29bcea'
        theme_text_color: 'Custom'
        md_bg_color: 0.09, 0.08, 0.08, 1
        text_color: 0.16, 0.77, 0.96, 1
        on_release: app.details_back()
    MDFloatingActionButton:
        icon: 'pencil'
        pos_hint: {'center_y': 0.95, 'center_x':0.85}
        theme_text_color: 'Custom'
        md_bg_color: 0.09, 0.08, 0.08, 1
        text_color: 0.16, 0.77, 0.96, 1
        on_release: app.edit_contact()
    MDFloatingActionButton:
        icon: 'trash-can'
        pos_hint: {'center_y': 0.95, 'center_x':0.95}
        icon_color: '#29bcea'
        theme_text_color: 'Custom'
        md_bg_color: 0.09, 0.08, 0.08, 1
        text_color: 0.16, 0.77, 0.96, 1
        on_release: app.delete_contact()
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            id: name
            size_hint: 1, 0.1
            pos_hint: {'center_y': 0.5, 'center_x':0.5}
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
<AddScreen>:
    name: 'add'
    MDFloatingActionButton:
        icon: 'arrow-left'
        pos_hint: {'center_y': 0.95}
        icon_color: '#29bcea'
        theme_text_color: 'Custom'
        md_bg_color: 0.09, 0.08, 0.08, 1
        text_color: 0.16, 0.77, 0.96, 1
        on_release: app.add_back()
    MDTextField:
        id: name
        hint_text: "Name"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.85}
        multiline: False
    MDTextField:
        id: description
        hint_text: "Description"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.75}
        multiline: True
    MDTextField:
        id: mobile1
        hint_text: "Mobile"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.65}
        multiline: False
    MDTextField:
        id: mobile2
        hint_text: "Mobile"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.55}
        multiline: False
    MDTextField:
        id: email
        hint_text: "Email"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.45}
        multiline: False
    MDTextField:
        id: address
        hint_text: "Address"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.35}
        multiline: True
    MDRectangleFlatButton:
        text: "Add"
        font_size: '18sp'
        pos_hint: {'center_x':0.5, 'center_y':0.25}
        on_release: app.add_contact_send(name.text, description.text, mobile1.text, mobile2.text, email.text, address.text)
<EditScreen>:
    name: 'edit'
    MDFloatingActionButton:
        icon: 'arrow-left'
        pos_hint: {'center_y': 0.95}
        icon_color: '#29bcea'
        theme_text_color: 'Custom'
        md_bg_color: 0.09, 0.08, 0.08, 1
        text_color: 0.16, 0.77, 0.96, 1
        on_release: app.edit_back()
    MDTextField:
        id: name
        hint_text: "Name"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.85}
        multiline: False
    MDTextField:
        id: description
        hint_text: "Description"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.75}
        multiline: True
    MDTextField:
        id: mobile1
        hint_text: "Mobile"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.65}
        multiline: False
    MDTextField:
        id: mobile2
        hint_text: "Mobile"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.55}
        multiline: False
    MDTextField:
        id: email
        hint_text: "Email"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.45}
        multiline: False
    MDTextField:
        id: address
        hint_text: "Address"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.35}
        multiline: True
    MDRectangleFlatButton:
        text: "Edit"
        font_size: '18sp'
        pos_hint: {'center_x':0.5, 'center_y':0.25}
        on_release: app.edit_contact_send(name.text, description.text, mobile1.text, mobile2.text, email.text, address.text)
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

class AddScreen(Screen):
    pass

class EditScreen(Screen):
    pass

class ContaXApp(MDApp):

    def build(self):
        self.icon = "icon1.png"
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        self.sm = ScreenManager(transition=SwapTransition())
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(ContactsScreen(name='list'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(DetailsScreen(name='details'))
        self.sm.add_widget(AddScreen(name='add'))
        self.sm.add_widget(EditScreen(name='edit'))
        
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

    def refresh_contacts(self):
        self.sm.get_screen('list').ids.contacts.clear_widgets()

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
        
        self.refresh_contacts()

    def register_screen(self):
        self.root.current = 'register'
    
    def back_to_login(self):
        self.sm.get_screen('register').ids.username.text = ""
        self.sm.get_screen('register').ids.email.text = ""
        self.sm.get_screen('register').ids.password.text = ""
        self.sm.get_screen('register').ids.password2.text = ""
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

    def refresh_details(self, id):
        self.current_contact_id = id
        self.sm.get_screen('details').ids.details.clear_widgets()
        response = requests.get(f"{details_url}{id}/",headers=self.headers)
        resp = response.json()
        self.sm.get_screen('details').ids.name.text = resp['name']
        self.sm.get_screen('details').ids.description.text = resp['description']

        if resp['mobile1']:
            lst_item = TwoLineIconListItem(
                    text = "Mobile",
                    secondary_text = resp['mobile1'],
                    on_release = partial(self.copy_details, resp['mobile1'])
                )
            lst_item.add_widget(IconLeftWidget(icon="phone"))
            self.sm.get_screen('details').ids.details.add_widget(lst_item)

        if resp['mobile2']:
            lst_item = TwoLineIconListItem(
                    text = "Mobile",
                    secondary_text = resp['mobile2'],
                    on_release = partial(self.copy_details, resp['mobile2'])
                )
            lst_item.add_widget(IconLeftWidget(icon="phone"))
            self.sm.get_screen('details').ids.details.add_widget(lst_item)

        if resp['email']:
            lst_item = TwoLineIconListItem(
                    text = "Email",
                    secondary_text = resp['email'],
                    on_release = partial(self.copy_details, resp['email'])
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
                    tertiary_text = "".join(lines[no_of_lines//2:]),
                    on_release = partial(self.copy_details, resp['address'])
                )
            lst_item.add_widget(IconLeftWidget(icon="home"))
            self.sm.get_screen('details').ids.details.add_widget(lst_item)

    def copy_details(self, tocopy, ele=None):
        Clipboard.copy(tocopy)

    def contact_details(self, id, ele=None):
        self.root.current = 'details'
        
        self.refresh_details(id)

    def list_back(self):
        self.sm.get_screen('list').ids.contacts.clear_widgets()
        self.root.current = 'login'

    def details_back(self):
        self.sm.get_screen('details').ids.details.clear_widgets()
        self.root.current = 'list'
        self.refresh_contacts()

    def add_back(self):
        self.sm.get_screen('add').ids.name.text = ""
        self.sm.get_screen('add').ids.description.text = ""
        self.sm.get_screen('add').ids.mobile1.text = ""
        self.sm.get_screen('add').ids.mobile2.text = ""
        self.sm.get_screen('add').ids.email.text = ""
        self.sm.get_screen('add').ids.address.text = ""
        self.root.current = 'list'
        self.refresh_contacts()

    def create_contact(self):
        self.root.current = 'add'

    def add_contact_send(self, name, desc, mob1, mob2, em, addr):
        flag = 0
        if name == "":
            check_string = "Invalid Data!"
            close_button = MDFlatButton(text="Close", on_release=self.close_add_dialog)
        
        else:
            self.sm.get_screen('add').ids.name.text = ""
            self.sm.get_screen('add').ids.description.text = ""
            self.sm.get_screen('add').ids.mobile1.text = ""
            self.sm.get_screen('add').ids.mobile2.text = ""
            self.sm.get_screen('add').ids.email.text = ""
            self.sm.get_screen('add').ids.address.text = ""
            
            contact_data = {
                "name": name,
                "description": desc,
                "mobile1": mob1,
                "mobile2": mob2,
                "email": em,
                "address": addr
            }

            response = requests.post(details_url, headers=self.headers, data=contact_data)
            flag = 1
            
            check_string = "Created contact successfully!"
            close_button = MDFlatButton(text="Close", on_release=self.close_add_dialog)

        self.add_dialog = MDDialog(title ="Add Contact", text=check_string, buttons=[close_button])
        if flag == 1:
            self.root.current = 'list'
            self.refresh_contacts()
        self.add_dialog.open()
        
    def close_add_dialog(self, obj):
        self.add_dialog.dismiss()

    def delete_contact(self):
        cancel_button = MDFlatButton(text="Cancel", on_release=self.close_confirmation_dialog)
        confirm_button = MDRaisedButton(text="Confirm", on_release=self.delete_confirmed)
        self.confirm_dialog = MDDialog(title="Confirm Delete", text="Are you sure you want to delete this contact?", buttons=[confirm_button, cancel_button])
        self.confirm_dialog.open()
    
    def close_confirmation_dialog(self, obj):
        self.confirm_dialog.dismiss()
    
    def delete_confirmed(self, obj):
        self.confirm_dialog.dismiss()
        c_id = self.current_contact_id
        response = requests.delete(f"{details_url}{c_id}/",headers=self.headers)
        self.root.current = 'list'
        self.refresh_contacts()

    def edit_contact(self):
        self.root.current= 'edit'
        c_id = self.current_contact_id
        response = requests.get(f"{details_url}{c_id}/",headers=self.headers)
        resp = response.json()
        self.sm.get_screen('edit').ids.name.text = resp['name']
        if resp['description']:
            self.sm.get_screen('edit').ids.description.text = resp['description']
        if resp['mobile1']:
            self.sm.get_screen('edit').ids.mobile1.text = resp['mobile1']
        if resp['mobile2']:
            self.sm.get_screen('edit').ids.mobile2.text = resp['mobile2']
        if resp['email']:
            self.sm.get_screen('edit').ids.email.text = resp['email']
        if resp['address']:
            self.sm.get_screen('edit').ids.address.text = resp['address']

    def edit_back(self):
        self.contact_details(self.current_contact_id)

    def edit_contact_send(self, name, desc, mob1, mob2, em, addr):
        c_id = self.current_contact_id
        flag = 0
        if name == "":
            check_string = "Invalid Data!"
            close_button = MDFlatButton(text="Close", on_release=self.close_edit_dialog)
        
        else:
            self.sm.get_screen('edit').ids.name.text = ""
            self.sm.get_screen('edit').ids.description.text = ""
            self.sm.get_screen('edit').ids.mobile1.text = ""
            self.sm.get_screen('edit').ids.mobile2.text = ""
            self.sm.get_screen('edit').ids.email.text = ""
            self.sm.get_screen('edit').ids.address.text = ""
            
            contact_data = {
                "name": name,
                "description": desc,
                "mobile1": mob1,
                "mobile2": mob2,
                "email": em,
                "address": addr
            }

            response = requests.put(f"{details_url}{c_id}/", headers=self.headers, data=contact_data)
            flag = 1
            
            check_string = "Editted contact successfully!"
            close_button = MDFlatButton(text="Close", on_release=self.close_edit_dialog)

        self.edit_dialog = MDDialog(title ="Edit Contact", text=check_string, buttons=[close_button])
        if flag == 1:
            self.root.current = 'details'
            self.refresh_details(c_id)
        self.edit_dialog.open()

    def close_edit_dialog(self, obj):
        self.edit_dialog.dismiss()

ContaXApp().run()