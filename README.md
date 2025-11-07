# 🔐 ImageShield — AES-Based Image Encryption Platform

**Author:** [Shreyash Killedar](https://github.com/Shreyash584)  
**Email:** [shreykilledar@gmail.com](mailto:shreykilledar@gmail.com)  
**Tech Stack:** Django · Python · AES Encryption · SHA-256 · TailwindCSS  

---

## 🧩 Overview

**ImageShield** is a secure web application built with Django that lets users **encrypt and decrypt images** using **AES (Advanced Encryption Standard)** and **SHA-256 hashing** for data integrity.  
It ensures that your uploaded image remains confidential and tamper-proof — all wrapped in a sleek, modern UI.

---

## 🧠 How It Works

### 🔒 Encryption
1. User uploads an image.
2. A unique 16-character AES key is generated automatically.
3. Image bytes are padded and encrypted using AES.
4. A SHA-256 hash of the original data is appended for integrity check.
5. The encrypted image is saved in the `/encrypted/` folder.

### 🔓 Decryption
1. User uploads the encrypted file and enters the AES key.
2. File is decrypted and verified against the SHA-256 hash.
3. If valid, the decrypted image is restored and saved in the `/uploads/` folder.

---

## 🗂️ Project Structure
ImageShield/
│
├── manage.py
├── imageshield/ # Project configuration (settings, urls, wsgi)
├── shield_app/ # Core app: views, utils, forms, etc.
├── templates/
│ └── shield_app/
│ └── index.html # Front-end (TailwindCSS UI)
├── media/
│ ├── encrypted/ # Encrypted images
│ └── uploads/ # Decrypted images
├── requirements.txt
└── .gitignore


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Shreyash584/ImageShield.git
cd ImageShield


