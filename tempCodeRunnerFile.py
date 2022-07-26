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
        BoxLayout:
            MDFlatButton:
                text: "Login"
                on_release: app.login(username.text, password.text)
            MDFlatButton:
                text: "Register"
                on_release: app.register_screen()