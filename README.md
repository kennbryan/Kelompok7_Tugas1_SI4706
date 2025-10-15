# 🛍️ JWT Marketplace API

**API Marketplace dengan autentikasi JWT (JSON Web Token)** menggunakan **FastAPI** dan **MySQL**.  
Proyek ini menyediakan fitur login, refresh token, pengambilan data marketplace, serta pembaruan profil pengguna dengan keamanan berbasis token.

---

## ⚙️ 1. Setup Environment & Menjalankan Server

### 🧩 Prasyarat

Pastikan kamu telah menginstal dan menyiapkan hal-hal berikut:

- **Python 3.10+**
- **MySQL / XAMPP**
- **pip** dan **venv** aktif
- **git** *(opsional)*

---

### 🚀 Langkah Instalasi

1. **Import folder project** ke komputer.
2. Buka **PowerShell** dan izinkan script berjalan:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Buat virtual environment**:
   ```bash
   python -m venv .venv
   ```
5. **Aktifkan environment**:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
6. **Pastikan library berikut sudah terinstal**:
   ```bash
   pip install bcrypt==4.0.1
   pip install email-validator
   ```
7. **Jalankan seeding data awal**:
   ```bash
   python scripts/seed.py
   ```
8. **Aktifkan MySQL/XAMPP** dan buat database:
   ```sql
   CREATE DATABASE jwt_marketplace;
   ```
9. **Jalankan server FastAPI**:
   ```bash
   python main.py
   ```
10. **Buka dokumentasi API di browser**:
    ```
    http://127.0.0.1:8000/docs
    ```

---

## 🔑 2. Variabel `.env` yang Diperlukan

Buat file **`.env`** di root project untuk menyimpan konfigurasi berikut:

| Variabel | Deskripsi |
|-----------|------------|
| `DATABASE_URL` | Connection string untuk menghubungkan aplikasi ke database |
| `JWT_SECRET` | Kunci rahasia JWT (digunakan untuk enkripsi token) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Waktu berlaku access token (menit) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Waktu berlaku refresh token (hari) |
| `PORT` | Port tempat server dijalankan |

**Contoh isi file `.env`:**
```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root@localhost:3306/jwt_marketplace

# JWT Configuration
JWT_SECRET=your_super_secret_key_change_this_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Server Configuration
PORT=8000
```

---

## 🧭 3. Daftar Endpoint & Skema Ringkas

| Method | Endpoint | Auth? | Deskripsi |
|--------|-----------|--------|------------|
| **POST** | `/auth/login` | ❌ | Login dan dapatkan `access_token` serta `refresh_token` |
| **POST** | `/auth/refresh` | ❌ | Refresh access token menggunakan `refresh_token` |
| **GET** | `/items` | ❌ | Ambil semua item yang tersedia di marketplace |
| **PUT** | `/profile` | ✅ JWT | Update profil pengguna (name/email) dan regenerasi token |

---

### 📤 Skema Request/Response

#### 🔹 `POST /auth/login`

**Request:**
```json
{
  "email": "user1@example.com",
  "password": "pass123"
}
```

**Response:**
```json
{
  "access_token": "<JWT_ACCESS>",
  "refresh_token": "<JWT_REFRESH>",
  "token_type": "bearer"
}
```

**Error (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

---

#### 🔹 `POST /auth/refresh`

**Request:**
```json
{
  "refresh_token": "<JWT_REFRESH>"
}
```

**Response:**
```json
{
  "access_token": "<NEW_JWT_ACCESS>",
  "refresh_token": "<JWT_REFRESH>",
  "token_type": "bearer"
}
```

---

#### 🔹 `GET /items`

**Response:**
```json
{
  "items": [
    { "id": 1, "name": "Sepatu Olahraga", "price": 250000 },
    { "id": 2, "name": "Kaos Polos", "price": 75000 }
  ]
}
```

---

#### 🔹 `PUT /profile`

**Header:**
```
Authorization: Bearer <JWT_ACCESS>
```

**Request:**
```json
{
  "name": "Nama Baru",
  "email": "new.email@example.com"
}
```

**Response:**
```json
{
  "message": "Profile updated",
  "profile": {
    "name": "Nama Baru",
    "email": "new.email@example.com"
  },
  "access_token": "<JWT_ACCESS>",
  "refresh_token": "<JWT_REFRESH>",
  "token_type": "bearer"
}
```

**Error (400 Bad Request):**
```json
{
  "error": "Email already in use"
}
```

**Error (401 Unauthorized):**
```json
{
  "error": "Missing or invalid Authorization header"
}
```

---

## 💻 4. Contoh Penggunaan cURL

### 🧩 4.1 Login

**Login Sukses:**
```bash
curl -X POST ^
  "http://127.0.0.1:8000/auth/login" ^
  -H "accept: application/json" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"user1@example.com\", \"password\":\"pass123\"}"
```

**Login Gagal (401):**
```bash
curl -Method POST "http://127.0.0.1:8000/auth/login" `
  -Headers @{ "accept" = "application/json"; "Content-Type" = "application/json" } `
  -Body '{"email": "user@example.com", "password": "salahpassword"}'
```

---

### 🔄 4.2 Refresh Token

**Refresh Sukses:**
```bash
curl -Method POST "http://127.0.0.1:8000/auth/refresh?refresh_token=<JWT_REFRESH>" `
  -Headers @{ "accept" = "application/json" } `
  -Body ''
```

**Refresh Gagal (token salah):**
```bash
curl -Method POST "http://127.0.0.1:8000/auth/refresh?refresh_token=<JWT_REFRESH_INVALID>" `
  -Headers @{ "accept" = "application/json" } `
  -Body ''
```

---

### 📦 4.3 Ambil Items

```bash
curl.exe -X GET "http://127.0.0.1:8000/items" -H "accept: application/json"
```

---

### 👤 4.4 Update Profil

**Update Profil Sukses:**
```bash
curl -Method PUT "http://127.0.0.1:8000/profile" `
  -Headers @{ 
      "accept" = "application/json"; 
      "Authorization" = "Bearer <JWT_ACCESS>"; 
      "Content-Type" = "application/json"
  } `
  -Body '{"name": "Ferdayy", "email": "user1@example.com"}'
```

**Gagal (tanpa token):**
```bash
curl -Method PUT "http://127.0.0.1:8000/profile" `
  -Headers @{ 
      "accept" = "application/json"; 
      "Content-Type" = "application/json"
  } `
  -Body '{"name": "Ferdayy", "email": "user1@example.com"}'
```

**Gagal (token kadaluarsa):**
```bash
curl -Method PUT "http://127.0.0.1:8000/profile" `
  -Headers @{ 
      "accept" = "application/json"; 
      "Authorization" = "Bearer <EXPIRED_JWT_ACCESS>"; 
      "Content-Type" = "application/json"
  } `
  -Body '{"name": "Ferdayy", "email": "user1@example.com"}'
```

---

## 🧠 5. Catatan & Asumsi

- Database **harus dibuat terlebih dahulu** sebelum menjalankan server, atau script `seed.py` akan gagal.
- `JWT_SECRET` **wajib diubah** menjadi string acak yang kuat sebelum digunakan di production.
- Saat **email user diubah**, token lama otomatis tidak valid dan diganti dengan token baru.
- Endpoint `/profile` memerlukan **Bearer token** yang valid pada header.
- Pada `PUT /profile`, minimal salah satu field (`name` atau `email`) harus diisi.

---

## 🧾 Lisensi

Proyek ini dibuat untuk kebutuhan tugas mata kuliah Integrasi Aplikasi Enterprise SI-47-06 Kelompok 7.

📌 **Author:**
1. Ferdiansyah Adi Saputra (102022330113)
2. Kennteh Bryan (102022330093)
3. Syarief Saleh Madhy (102022300201)
4. I Gusti Ngurah Raja Putra Bumi (102022300159)