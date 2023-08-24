import tkinter as tk
import tkinter.ttk as ttk
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime


class DovizAltinUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Döviz ve Altın Uygulaması")

        self.options = Options()
        self.driver = webdriver.Firefox(options=self.options)

        self.tree = ttk.Treeview(root, columns=("Site", "Bilgi", "Değer", "Durum"), show="headings")
        self.tree.heading("Site", text="Site")
        self.tree.heading("Bilgi", text="Bilgi")
        self.tree.heading("Değer", text="Değer")
        self.tree.heading("Durum", text="Durum")

        self.tree.tag_configure("oddrow", background="#f0f0f0")
        self.tree.tag_configure("evenrow", background="#ffffff")

        self.tree.pack()

        self.update_button = tk.Button(root, text="Güncelle", command=self.update_prices)
        self.update_button.pack()

        self.last_update_label = tk.Label(root, text="Son Güncelleme: -")
        self.last_update_label.pack(side="right", padx=10, pady=5)


        self.doviz_url = "https://kur.doviz.com/serbest-piyasa/euro"
        self.doviz2_url = "https://kur.doviz.com/serbest-piyasa/amerikan-dolari"
        self.doviz3_url = "https://altin.doviz.com/gram-altin"
        self.altin_in_url2 = "https://altin.in/fiyat/gram-altin"
        self.altin_in_url3 = "https://yorum.altin.in/tum/dolar"
        self.altin_in_url4 = "https://yorum.altin.in/tum/euro"
        self.nadir_url1 = "https://www.nadirdoviz.com/parite.aspx?grupid=1&p=AU/TL"
        self.nadir_url2 = "https://www.nadirdoviz.com/parite.aspx?grupid=2&p=USD/TL"
        self.nadir_url3 = "https://www.nadirdoviz.com/parite.aspx?grupid=2&p=EUR/TL"

        self.old_data = {}


        self.update_prices()

    def get_euro_price(self):
        self.driver.get(self.doviz_url)
        euro_element = WebDriverWait(self.driver, 2).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-socket-key='EUR'][data-socket-attr='s']"))
        )
        return euro_element.text

    def get_dollar_price(self):
        self.driver.get(self.doviz2_url)
        dollar_element = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-socket-key='USD'][data-socket-attr='s']"))
        )
        return dollar_element.text

    def get_gram_altin_price(self):
        self.driver.get(self.doviz3_url)
        gram_element = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-socket-key='gram-altin'][data-socket-attr='s']"))
        )
        return gram_element.text

    def get_gram_altin_price2(self):
        try:
            self.driver.get(self.altin_in_url2)
            gram_altin_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div[title='Gram Altın'] li.midrow.alis"))
            )
            gram_altin_price2 = float(gram_altin_element.text.replace(",", ""))
            return gram_altin_price2
        except Exception as e:
            return None

    def get_parite_value(self):
        self.driver.get(self.altin_in_url4)
        parite_element = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "parite"))
        )
        parite_value = parite_element.find_element(By.CSS_SELECTOR, "h2#pfiy").text
        return parite_value


    def get_euro_value_altin(self):
        self.driver.get(self.altin_in_url4)
        euro_element2 = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "euro"))
        )
        euro_value = euro_element2.find_element(By.CSS_SELECTOR, "h2#efiy").text
        return euro_value

    def get_dollar_value_altin(self):
        self.driver.get(self.altin_in_url3)
        dolar_element2 = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "dolar"))
        )
        dollar_value = dolar_element2.find_element(By.CSS_SELECTOR, "h2#dfiy").text
        return dollar_value

    def get_parite_value_nadir(self):
        self.driver.get(self.nadir_url1)
        try:
            parite_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "tr[data-symbol='D1'] td.fadg"))
            )
            parite_value = parite_element.text
            return parite_value
        except Exception as e:
            print("Hata:", e)
            return None

    def get_dollar_value_nadir(self):
        self.driver.get(self.nadir_url2)
        try:
            usd_tl_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "tr[data-symbol='D4'] td.fadg"))
            )
            usd_tl_value = usd_tl_element.text
            return usd_tl_value
        except Exception as e:
            print("Hata:", e)
            return None

    def get_euro_value_nadir(self):
        self.driver.get(self.nadir_url3)
        try:
            eur_tl_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "tr[data-symbol='D5'] td.fadg"))
            )
            eur_tl_value = eur_tl_element.text
            return eur_tl_value
        except Exception as e:
            print("Hata:", e)
            return None

    def update_prices(self):
        data = [
            ("altin.in", "Parite Değeri", self.get_parite_value()),
            ("altin.in", "EURO/TL", self.get_euro_value_altin()),
            ("nadirdoviz", "EURO/TL", self.get_euro_value_nadir()),
            ("doviz.com", "EURO/TL", self.get_euro_price()),
            ("altin.in", "USD/TL", self.get_dollar_value_altin()),
            ("nadirdoviz", "USD/TL", self.get_dollar_value_nadir()),
            ("doviz.com", "USD/TL", self.get_dollar_price()),
            ("altin.in", "ALTIN/TL", self.get_gram_altin_price2()),
            ("nadirdoviz", "ALTIN/TL", self.get_parite_value_nadir()),
            ("doviz.com", "ALTIN/TL", self.get_gram_altin_price()),
        ]

        self.tree.delete(*self.tree.get_children())
        for index, (site, bilgi, deger) in enumerate(data):
            tag = "evenrow" if index % 2 == 0 else "oddrow"

            if site in self.old_data and bilgi in self.old_data[site]:
                old_value = float(str(self.old_data[site][bilgi]).replace(",", ""))
                if isinstance(deger, str):
                    new_value = float(deger.replace(",", ""))
                else:
                    new_value = deger
                change = new_value - old_value

                if old_value != 0:
                    percent_change = (change / old_value) * 100
                else:
                    percent_change = 0

                status = ""
                if percent_change > 0:
                    status = f"🔼 (+{percent_change:.2f}%)"
                elif percent_change < 0:
                    status = f"🔽 ({percent_change:.2f}%)"
                else:
                    status = "-"

                self.tree.insert("", "end", values=(site, bilgi, deger, status), tags=(tag,))
                self.old_data[site][bilgi] = deger
            else:
                self.old_data.setdefault(site, {})[bilgi] = deger
                self.tree.insert("", "end", values=(site, bilgi, deger, "-"), tags=(tag,))

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_update_label.config(text="Son Güncelleme: " + current_time)

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = DovizAltinUygulamasi(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()