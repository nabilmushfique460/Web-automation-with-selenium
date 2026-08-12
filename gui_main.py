import os
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class DemoQAAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DemoQA Automation Bot")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # --- Login Credentials Frame ---
        login_frame = ttk.LabelFrame(self.root, text="1. Login Credentials")
        login_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.login_user_entry = ttk.Entry(login_frame, width=30)
        self.login_user_entry.insert(0, "nabil29089")
        self.login_user_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.login_pass_entry = ttk.Entry(login_frame, width=30, show="*")
        self.login_pass_entry.insert(0, "Nabil371#")
        self.login_pass_entry.grid(row=1, column=1, padx=5, pady=5)

        # --- Fake Data Frame ---
        data_frame = ttk.LabelFrame(self.root, text="2. Text Box Fake Data")
        data_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(data_frame, text="Full Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(data_frame, width=40)
        self.name_entry.insert(0, "John Doe")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(data_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(data_frame, width=40)
        self.email_entry.insert(0, "johndoe@fakeemail.com")
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(data_frame, text="Current Address:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.cur_addr_entry = ttk.Entry(data_frame, width=40)
        self.cur_addr_entry.insert(0, "123 Fake Street, Springfield")
        self.cur_addr_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(data_frame, text="Permanent Address:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.perm_addr_entry = ttk.Entry(data_frame, width=40)
        self.perm_addr_entry.insert(0, "456 Real Avenue, Shelbyville")
        self.perm_addr_entry.grid(row=3, column=1, padx=5, pady=5)

        # --- Run Button ---
        self.run_btn = ttk.Button(self.root, text="Start Automation", command=self.start_automation_thread)
        self.run_btn.pack(pady=10)

        # --- Log Output ---
        log_frame = ttk.LabelFrame(self.root, text="Execution Logs")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10, state='disabled')
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)

    def log(self, message):
        """Helper to print messages to the GUI log safely"""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.root.update()

    def start_automation_thread(self):
        """Starts the automation in a background thread to prevent GUI freezing"""
        self.run_btn.config(state=tk.DISABLED)
        self.log("--- Starting Automation ---")

        # Grab data from inputs before starting thread
        data = {
            "user": self.login_user_entry.get(),
            "pass": self.login_pass_entry.get(),
            "name": self.name_entry.get(),
            "email": self.email_entry.get(),
            "cur_addr": self.cur_addr_entry.get(),
            "perm_addr": self.perm_addr_entry.get()
        }

        # Run Selenium in a separate thread
        thread = threading.Thread(target=self.run_selenium, args=(data,), daemon=True)
        thread.start()

    def run_selenium(self, data):
        driver = None
        try:
            download_dir = os.getcwd()
            self.log(f"Setting download directory to: {download_dir}")

            chrome_options = Options()
            chrome_options.add_argument("--disable-search-engine-choice-screen")

            # Keep browser open for a few seconds at the end to see the result
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)

            # NOTE: Update the path if chromedriver is not in this exact directory
            service = Service('chromedriver-win64/chromedriver.exe')

            self.log("Launching Chrome Browser...")
            driver = webdriver.Chrome(options=chrome_options, service=service)

            # 1. Login
            self.log("Navigating to login page...")
            driver.get('https://demoqa.com/login')

            username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'userName')))
            password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'password')))
            login_button = driver.find_element(By.ID, 'login')

            self.log("Submitting login credentials...")
            username_field.send_keys(data["user"])
            password_field.send_keys(data["pass"])
            driver.execute_script("arguments[0].click();", login_button)

            # 2. Elements Accordion
            self.log("Opening Elements menu...")
            elements = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Elements']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elements)
            driver.execute_script("arguments[0].click();", elements)

            # 3. Text Box
            self.log("Opening Text Box page...")
            text_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Text Box']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", text_box)
            driver.execute_script("arguments[0].click();", text_box)

            # 4. Fill Form
            self.log("Filling fake data...")
            full_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'userName')))
            email = driver.find_element(By.ID, 'userEmail')
            current_address = driver.find_element(By.ID, 'currentAddress')
            permanent_address = driver.find_element(By.ID, 'permanentAddress')
            submit_button = driver.find_element(By.ID, 'submit')

            full_name.send_keys(data["name"])
            email.send_keys(data["email"])
            current_address.send_keys(data["cur_addr"])
            permanent_address.send_keys(data["perm_addr"])

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
            driver.execute_script("arguments[0].click();", submit_button)
            self.log("Form submitted successfully!")

            # 5. Upload & Download
            self.log("Navigating to Upload and Download page...")
            upload_download_menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Upload and Download']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", upload_download_menu)
            driver.execute_script("arguments[0].click();", upload_download_menu)

            # 6. Download
            self.log("Triggering download...")
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'downloadButton'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
            driver.execute_script("arguments[0].click();", download_button)

            self.log(f"Success! File downloading to: {download_dir}")
            messagebox.showinfo("Success", "Automation completed successfully!")

        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

        finally:
            if driver:
                self.log("Closing browser...")
                driver.quit()

            # Re-enable the run button
            self.run_btn.config(state=tk.NORMAL)
            self.log("--- Automation Finished ---")


if __name__ == "__main__":
    root = tk.Tk()
    app = DemoQAAutomationApp(root)
    root.mainloop()