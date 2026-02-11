from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.core.window import Window
from decimal import Decimal, getcontext

Window.size = (360, 640)
getcontext().prec = 50

class HesaplayiciApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.active_input = "fiyat"
        self.raw_values = {"fiyat": "0", "tutar": "0", "miktar": "0"}
        self.sifir_btn = None
        
        screen = MDScreen()
        main_layout = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10), md_bg_color=(0.96, 0.96, 0.96, 1))

        main_layout.add_widget(MDLabel(
            text="HESAPLAYICI", halign="center", font_style="H4", 
            theme_text_color="Custom", text_color=(1, 0, 0, 1), bold=True, size_hint_y=None, height=dp(70)
        ))

        self.inputs = {}
        for label_text, key in [("FİYAT", "fiyat"), ("TUTAR", "tutar"), ("MİKTAR", "miktar")]:
            row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
            lbl = MDLabel(text=label_text, theme_text_color="Custom", text_color=(1, 0, 0, 1), bold=True, size_hint_x=0.25)
            
            box = MDRaisedButton(
                text="0", md_bg_color=(0.55, 0.55, 0.55, 1), size_hint_x=0.75, elevation=2,
                on_release=lambda x, k=key: self.set_active(k)
            )
            self.inputs[key] = box
            row.add_widget(lbl)
            row.add_widget(box)
            main_layout.add_widget(row)

        grid = MDGridLayout(cols=4, spacing=dp(8), size_hint_y=None, height=dp(280), padding=0)
        tuslar = [
            'Sil', '←', '+', '-',
            '1', '2', '3', '×',
            '4', '5', '6', '÷',
            '7', '8', '9', ','
        ]
        for t in tuslar:
            btn = MDRaisedButton(
                text=t, size_hint=(1, 1), md_bg_color=(0.88, 0.88, 0.88, 1), 
                text_color=(0, 0, 0, 1), font_style="H6",
                on_release=self.tus_basildi
            )
            grid.add_widget(btn)
        
        main_layout.add_widget(grid)

        alt_satir = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=0,
            spacing=0
        )
        
        self.sifir_btn = MDRaisedButton(
            text="0",
            size_hint=(1, 1),
            md_bg_color=(0.88, 0.88, 0.88, 1),
            text_color=(0, 0, 0, 1),
            font_style="H6",
            elevation=2,
            on_release=self.sifir_tiklandi
        )
        
        alt_satir.add_widget(self.sifir_btn)
        main_layout.add_widget(alt_satir)
        
        screen.add_widget(main_layout)
        return screen

    def sifir_tiklandi(self, instance):
        current_raw = self.raw_values[self.active_input]
        
        if current_raw == "0":
            self.raw_values[self.active_input] = "0"
        else:
            self.raw_values[self.active_input] += "0"
        
        self.hesapla_hepsini()

    def set_active(self, key):
        self.active_input = key
        for k in self.inputs: 
            self.inputs[k].md_bg_color = (0.55, 0.55, 0.55, 1)
        self.inputs[key].md_bg_color = (0.35, 0.35, 0.35, 1)

    def format_gosterim(self, n):
        try:
            d = Decimal(str(n))
            s = "{:,.5f}".format(d).rstrip('0').rstrip('.')
            parts = s.split('.')
            parts[0] = parts[0].replace(',', '.')
            return ",".join(parts) if len(parts) > 1 else parts[0]
        except: 
            return "0"

    def hesapla_hepsini(self):
        try:
            f = Decimal(self.raw_values["fiyat"].replace(",", "."))
            t = Decimal(self.raw_values["tutar"].replace(",", "."))
            m = Decimal(self.raw_values["miktar"].replace(",", "."))
            
            if self.active_input == "fiyat" or self.active_input == "miktar":
                t = f * m
                self.raw_values["tutar"] = str(t)
            elif self.active_input == "tutar":
                if f > 0:
                    m = t / f
                    self.raw_values["miktar"] = str(m)
            
            for k in self.inputs: 
                self.inputs[k].text = self.format_gosterim(self.raw_values[k])
        except: 
            pass

    def tus_basildi(self, instance):
        tus = instance.text.strip()
        current_raw = self.raw_values[self.active_input]
        
        if tus in '0123456789':
            if current_raw == "0": 
                self.raw_values[self.active_input] = tus
            else: 
                self.raw_values[self.active_input] += tus
        elif tus == ',':
            if ',' not in current_raw: 
                self.raw_values[self.active_input] += ','
        elif tus == '←':
            self.raw_values[self.active_input] = current_raw[:-1] if len(current_raw) > 1 else "0"
        elif tus == 'Sil':
            self.raw_values[self.active_input] = "0"
        
        self.hesapla_hepsini()

if __name__ == "__main__":
    HesaplayiciApp().run()
