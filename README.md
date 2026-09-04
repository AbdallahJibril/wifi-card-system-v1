# 📶 Network Wi-Fi Cards Management System (v1 - Monolith)

A monolithic backend and management system built for generating, tracking, and auditing Wi-Fi access cards. This project was developed as a hands-on training project to master backend architecture, security practices, and database management.

---

## 🚀 Features & Capabilities

* **Admin Authentication:** Secure login system with password hashing.
* **Account Creation & Management:** Admin registration with strict username uniqueness validation (`Unique Constraints`).
* **Wi-Fi Card Generation:** Dynamic card generator allowing custom code length, total codes, usage limits, and duration/time configuration.
* **Card Lifecycle Tracking:** 
  * Checks card status (Active, Expired, Disabled, or Not Found).
  * Automatically increments usage counters upon successful validation.
  * Migrates cards to a "used/expired list" once their usage limit is reached.
* **System Audit Trail & Logging:** Comprehensive system logs tracking all critical actions (logins, account creations, card generations, password changes) along with their success/failure status and timestamps.
* **Admin Controls:** Ability to add new administrators, update credentials (usernames/passwords with validation), and view comprehensive activity logs.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Web Framework:** Flask
* **Database:** MySQL (phpMyAdmin)
* **Security:** Password Hashing

---

## ⚙️ How to Run Locally

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/AbdallahJibril/wifi-card-system-v1.git](git@github.com:AbdallahJibril/wifi-card-system-v1.git)
   cd wifi-card-system-v1
2. Setup Database:
​Create a new database in MySQL/phpMyAdmin.
​Import the provided structure file (database.sql) into your database.
3. Run the Application:python app.py

