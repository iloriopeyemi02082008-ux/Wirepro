# WirePro World Edition - By opezzy
# Tech Electrician App
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.storage.jsonstore import JsonStore
import math
from datetime import datetime

# Default prices per country
COUNTRY_DATA = {
    "Nigeria (NGN)": {"currency": "N", "prices": {"1.5mm": 450, "2.5mm": 700, "4.0mm": 1100, "6.0mm": 1700, "10mm": 2800, "16mm": 4500}},
    "Ghana (GHS)": {"currency": "GHs", "prices": {"1.5mm": 15, "2.5mm": 25, "4.0mm": 40, "6.0mm": 65, "10mm": 110, "16mm": 180}},
    "Kenya (KES)": {"currency": "KSh", "prices": {"1.5mm": 120, "2.5mm": 200, "4.0mm": 350, "6.0mm": 550, "10mm": 900, "16mm": 1500}},
    "India (INR)": {"currency": "Rs", "prices": {"1.5mm": 25, "2.5mm": 40, "4.0mm": 65, "6.0mm": 110, "10mm": 180, "16mm": 300}},
    "USA (USD)": {"currency": "$", "prices": {"1.5mm": 0.8, "2.5mm": 1.2, "4.0mm": 2.0, "6.0mm": 3.5, "10mm": 6, "16mm": 10}},
    "UK (GBP)": {"currency": "£", "prices": {"1.5mm": 0.7, "2.5mm": 1.0, "4.0mm": 1.8, "6.0mm": 3.0, "10mm": 5, "16mm": 9}},
}

store = JsonStore('wirepro_settings.json')

def get_wire(amps):
    if amps <= 5: return "1.5mm"
    elif amps <= 10: return "2.5mm"
    elif amps <= 20: return "4.0mm"
    elif amps <= 30: return "6.0mm"
    elif amps <= 45: return "10mm"
    else: return "16mm"

class WireProApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.layout.add_widget(Label(text="WirePro - World Electrician", font_size=22, size_hint_y=0.2))
        
        self.customer_input = TextInput(hint_text="Customer Name", multiline=False)
        self.amps_input = TextInput(hint_text="Load Current (Amps)", input_filter='float', multiline=False)
        self.dist_input = TextInput(hint_text="Distance (meters)", input_filter='float', multiline=False)
        self.result_label = Label(text="Enter details and Calculate", font_size=16)
        
        self.layout.add_widget(self.customer_input)
        self.layout.add_widget(self.amps_input)
        self.layout.add_widget(self.dist_input)
        
        calc_btn = Button(text="CALCULATE & SHARP PRICE", background_color=(0,0.7,0,1))
        calc_btn.bind(on_press=self.calculate)
        
        settings_btn = Button(text="Settings - Change Price/Currency", background_color=(0.2,0.2,0.8,1), size_hint_y=0.3)
        settings_btn.bind(on_press=self.open_settings)
        
        self.layout.add_widget(calc_btn)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(settings_btn)
        
        # Check first time
        if not store.exists('setup'):
            self.open_first_time_setup()
            
        return self.layout

    def get_current_settings(self):
        if store.exists('setup'):
            return store.get('setup')
        else:
            return COUNTRY_DATA["Nigeria (NGN)"]

    def open_first_time_setup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Welcome! First Time Setup"))
        
        spinner = Spinner(text="Nigeria (NGN)", values=list(COUNTRY_DATA.keys()), size_hint_y=0.3)
        content.add_widget(spinner)
        
        info = Label(text="Select your country. You can change prices later in Settings.", font_size=12)
        content.add_widget(info)
        
        def save_setup(instance):
            country = spinner.text
            store.put('setup', country=country, currency=COUNTRY_DATA[country]["currency"], prices=COUNTRY_DATA[country]["prices"])
            popup.dismiss()
        
        btn = Button(text="Save & Start", size_hint_y=0.3)
        btn.bind(on_press=save_setup)
        content.add_widget(btn)
        
        popup = Popup(title="WirePro Setup", content=content, size_hint=(0.9,0.7), auto_dismiss=False)
        popup.open()

    def open_settings(self, instance):
        content = BoxLayout(orientation='vertical', spacing=5, padding=10)
        settings = self.get_current_settings()
        
        content.add_widget(Label(text=f"Country: {settings['country']} | Currency: {settings['currency']}"))
        content.add_widget(Label(text="Edit Wire Price Per Meter:"))
        
        inputs = {}
        for size, price in settings['prices'].items():
            row = BoxLayout(size_hint_y=0.2)
            row.add_widget(Label(text=size))
            ti = TextInput(text=str(price), input_filter='float', multiline=False)
            inputs[size] = ti
            row.add_widget(ti)
            content.add_widget(row)
        
        def save_prices(instance):
            new_prices = {size: float(inp.text) for size, inp in inputs.items()}
            store.put('setup', country=settings['country'], currency=settings['currency'], prices=new_prices)
            popup.dismiss()
            self.result_label.text = "Prices Updated!"
        
        save_btn = Button(text="Save New Prices", background_color=(0,0.7,0,1), size_hint_y=0.3)
        save_btn.bind(on_press=save_prices)
        content.add_widget(save_btn)
        
        popup = Popup(title="Settings - Wire Prices", content=content, size_hint=(0.9,0.9))
        popup.open()

    def calculate(self, instance):
        try:
            settings = self.get_current_settings()
            amps = float(self.amps_input.text)
            dist = float(self.dist_input.text)
            wire = get_wire(amps)
            breaker = int(amps * 1.25)
            
            price_per_m = settings['prices'].get(wire, 1000)
            raw = price_per_m * dist * 1.1
            labour = raw * 0.1
            total = raw + labour
            sharp = math.ceil(total / 500) * 500
            cur = settings['currency']
            
            self.result_label.text = f"{wire} | Breaker {breaker}A\nRaw: {cur}{total:.0f}\nSHARP: {cur}{sharp}"
            
            # Save quote log
            try:
                with open("quotes.txt", "a") as f:
                    f.write(f"{self.customer_input.text} - {wire} {dist}m = {cur}{sharp} - {datetime.now().strftime('%d/%m')}\n")
            except: pass
            
        except Exception as e:
            self.result_label.text = "Enter valid Amps & Distance"

WireProApp().run()