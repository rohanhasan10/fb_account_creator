import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# ডাটা স্ট্রাকচার
ACCOUNTS_FILE = "accounts.json"
os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    return {"numbers": [], "accounts": []}

def save_data(data):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def show_menu():
    print("""
    ███████╗ █████╗ ██████╗ ███████╗██████╗ 
    ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗
    █████╗  ███████║██████╔╝█████╗  ██████╔╝
    ██╔══╝  ██╔══██║██╔══██╗██╔══╝  ██╔══██╗
    ██║     ██║  ██║██║  ██║███████╗██║  ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    Facebook Account Creator Tool
    """)
    print("1. 📥 Add Number")
    print("2. 🗑️ Delete Number")
    print("3. 🛠️ Create Accounts (5/10/20)")
    print("4. 🚪 Exit")
    print("-"*40)

def add_number(data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("📥 Add Phone Number\n")
    print("নাম্বার ফরম্যাট: +8801712345678 (কান্ট্রি কোড সহ)")
    numbers = input("\nনাম্বার গুলো লিখুন (কমা দিয়ে আলাদা করুন): ").strip()
    
    new_numbers = [num.strip() for num in numbers.split(',') if num.strip()]
    data['numbers'].extend(new_numbers)
    save_data(data)
    
    print(f"\n✔ {len(new_numbers)} টি নাম্বার সফলভাবে যোগ হয়েছে!")
    time.sleep(2)

def delete_number(data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🗑️ Delete Phone Number\n")
    
    if not data['numbers']:
        print("কোন নাম্বার নেই ডিলেট করার জন্য!")
        time.sleep(2)
        return
    
    for i, num in enumerate(data['numbers'], 1):
        print(f"{i}. {num}")
    
    try:
        choice = int(input("\nকোন নাম্বার ডিলেট করতে চান (নম্বর দিন): ")) - 1
        if 0 <= choice < len(data['numbers']):
            deleted = data['numbers'].pop(choice)
            save_data(data)
            print(f"\n✔ {deleted} ডিলেট হয়েছে!")
        else:
            print("\n❌ ভুল ইনপুট!")
    except:
        print("\n❌ ভুল ইনপুট!")
    
    time.sleep(2)

def create_accounts(data):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🛠️ Create Accounts\n")
    
    if not data['numbers']:
        print("কোন নাম্বার নেই! প্রথমে নাম্বার যোগ করুন")
        time.sleep(2)
        return
    
    print("কতগুলো একাউন্ট খুলবেন?")
    print("1. 5 টি একাউন্ট")
    print("2. 10 টি একাউন্ট")
    print("3. 20 টি একাউন্ট")
    print("4. কাস্টম সংখ্যা")
    
    try:
        choice = int(input("\nআপনার পছন্দ: "))
        if choice == 1:
            count = 5
        elif choice == 2:
            count = 10
        elif choice == 3:
            count = 20
        elif choice == 4:
            count = int(input("কতগুলো একাউন্ট খুলবেন: "))
            if count > 20:
                print("সর্বোচ্চ ২০ টি একাউন্ট খোলা যাবে")
                count = 20
        else:
            print("ভুল ইনপুট!")
            return
    except:
        print("ভুল ইনপুট!")
        return
    
    numbers_to_use = data['numbers'][:count]
    otp_codes = {}
    
    # প্রথমে সব নাম্বারে OTP পাঠানো
    driver = webdriver.Firefox()
    try:
        for num in numbers_to_use:
            print(f"\nOTP পাঠানো হচ্ছে: {num}")
            driver.get("https://m.facebook.com/reg")
            
            # ফর্ম ফিলাপ
            driver.find_element(By.NAME, "firstname").send_keys("Test")
            driver.find_element(By.NAME, "lastname").send_keys("User")
            driver.find_element(By.NAME, "reg_email__").send_keys(num)
            driver.find_element(By.NAME, "reg_passwd__").send_keys("Test@1234")
            
            # জন্ম তারিখ
            Select(driver.find_element(By.ID, "day")).select_by_value("15")
            Select(driver.find_element(By.ID, "month")).select_by_value("6")
            Select(driver.find_element(By.ID, "year")).select_by_value("1990")
            
            # লিঙ্গ নির্বাচন
            driver.find_element(By.XPATH, "//input[@value='2']").click()
            
            driver.find_element(By.NAME, "websubmit").click()
            time.sleep(3)
            
            if "verify" in driver.current_url:
                otp_codes[num] = ""
                print(f"✔ OTP পাঠানো হয়েছে: {num}")
            else:
                print(f"❌ OTP পাঠানো যায়নি: {num}")
            
            time.sleep(2)
    
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()
    
    # OTP গুলো সংগ্রহ
    os.system('cls' if os.name == 'nt' else 'clear')
    print("📲 OTP Verification\n")
    for num in otp_codes:
        otp_codes[num] = input(f"{num} - OTP টি দিন: ").strip()
    
    # একাউন্ট ভেরিফিকেশন
    driver = webdriver.Firefox()
    success = 0
    failed = 0
    
    try:
        for num, otp in otp_codes.items():
            print(f"\nভেরিফাই করা হচ্ছে: {num}")
            driver.get("https://m.facebook.com/confirmemail.php")
            
            # OTP ফিল্ড খুঁজে
            try:
                driver.find_element(By.NAME, "code").send_keys(otp)
                driver.find_element(By.NAME, "confirm").click()
                time.sleep(5)
                
                if "welcome" in driver.current_url:
                    account = {
                        "number": num,
                        "password": "Test@1234",
                        "date": str(datetime.now()),
                        "status": "success"
                    }
                    data['accounts'].append(account)
                    save_data(data)
                    success += 1
                    print(f"✔ সফল: {num}")
                else:
                    failed += 1
                    print(f"❌ ব্যর্থ: {num}")
            except:
                failed += 1
                print(f"❌ OTP ভুল: {num}")
            
            time.sleep(2)
    
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()
    
    # ফলাফল দেখানো
    print("\n" + "="*40)
    print(f"মোট চেষ্টা: {len(otp_codes)}")
    print(f"সফল: {success}")
    print(f"ব্যর্থ: {failed}")
    print("="*40)
    
    input("\nএন্টার চাপুন মেনুতে ফিরে যেতে...")

def main():
    data = load_data()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        show_menu()
        
        choice = input("আপনার পছন্দ: ")
        
        if choice == '1':
            add_number(data)
        elif choice == '2':
            delete_number(data)
        elif choice == '3':
            create_accounts(data)
        elif choice == '4':
            print("\nটুল বন্ধ হচ্ছে...")
            break
        else:
            print("\n❌ ভুল ইনপুট! আবার চেষ্টা করুন")
            time.sleep(1)

if __name__ == "__main__":
    main()
