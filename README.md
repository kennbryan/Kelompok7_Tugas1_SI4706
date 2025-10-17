# 🛍️ JWT Marketplace API

**API Marketplace dengan autentikasi JWT (JSON Web Token)** menggunakan **FastAPI** dan **MySQL**.  
Proyek ini menyediakan fitur login, refresh token, pengambilan data marketplace, serta pembaruan profil pengguna dengan keamanan berbasis token.

---

## 1. Setup Environment & Menjalankan Server

### Prasyarat

Pastikan kamu telah menginstal dan menyiapkan hal-hal berikut:

- **Python 3.10+**
- **MySQL / XAMPP**
- **pip** dan **venv** aktif
- **git** *(opsional)*

---

### Langkah Instalasi

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

## 2. Variabel `.env` yang Diperlukan

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

## 3. Daftar Endpoint & Skema Ringkas

| Method | Endpoint | Auth? | Deskripsi |
|--------|-----------|--------|------------|
| **POST** | `/auth/login` | ❌ | Login dan dapatkan `access_token` serta `refresh_token` |
| **POST** | `/auth/refresh` | ❌ | Refresh access token menggunakan `refresh_token` |
| **GET** | `/items` | ❌ | Ambil semua item yang tersedia di marketplace |
| **PUT** | `/profile` | ✅ JWT | Update profil pengguna (name/email) dan regenerasi token |

---

### Skema Request/Response

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
<img width="1383" height="779" alt="Image" src="https://github.com/user-attachments/assets/ab2c2d5f-e618-4db4-80aa-b53e6eed3ebb" />
<br>
<br>

**Error (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```
<img width="1377" height="530" alt="Image" src="https://github.com/user-attachments/assets/4ca85614-d9ae-49f8-9961-d48c88a1bbab" />

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
<img width="1379" height="713" alt="Image" src="https://github.com/user-attachments/assets/7cf8fac7-45b1-4156-a180-63c69031af3a" />

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
<img width="1378" height="788" alt="Image" src="https://github.com/user-attachments/assets/c250c1f7-16cd-4edd-9d5a-77d6fed4b5ea" />

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
<img width="1367" height="760" alt="Image" src="https://github.com/user-attachments/assets/a69e03e6-4a82-499f-a571-1e24c9f97e55" />
<br>
<br>

**Error (400 Bad Request):**
```json
{
  "error": "Email already in use"
}
```
<img width="1373" height="512" alt="Image" src="https://github.com/user-attachments/assets/1cdcda28-2f38-4008-9c12-89ea01266927" />
<br>
<br>

**Error (401 Unauthorized):**
```json
{
  "error": "Missing or invalid Authorization header"
}
```
<img width="1382" height="509" alt="Image" src="https://github.com/user-attachments/assets/1074723f-49cb-4fdf-9be5-e84dc17a2288" />

---

## 4. Contoh Penggunaan cURL

### 4.1 Login

**Login Sukses:**
```bash
curl -X POST ^
  "http://127.0.0.1:8000/auth/login" ^
  -H "accept: application/json" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"user1@example.com\", \"password\":\"pass123\"}"
```
<img width="1480" height="332" alt="Image" src="https://github.com/user-attachments/assets/ded0631a-5be4-4880-ae71-d07c8ebafc7c" />

**Login Gagal (401):**
```bash
curl -Method POST "http://127.0.0.1:8000/auth/login" `
  -Headers @{ "accept" = "application/json"; "Content-Type" = "application/json" } `
  -Body '{"email": "user@example.com", "password": "salahpassword"}'
```
<img width="1642" height="72" alt="Image" src="https://github.com/user-attachments/assets/5e48a804-eb8d-4e6a-9c48-b70e6214ef75" />

---

### 4.2 Refresh Token

**Refresh Sukses:**
```bash
curl -Method POST "http://127.0.0.1:8000/auth/refresh?refresh_token=<JWT_REFRESH>" `
  -Headers @{ "accept" = "application/json" } `
  -Body ''
```
<img width="1633" height="341" alt="Image" src="https://github.com/user-attachments/assets/6ced6c4b-44c6-4b39-8816-e8b04e00d485" />

**Refresh Gagal (token salah):**
```bash
curl -Method POST "http://127.0.0.1:8000/auth/refresh?refresh_token=<JWT_REFRESH_INVALID>" `
  -Headers @{ "accept" = "application/json" } `
  -Body ''
```
<img width="1621" height="99" alt="Image" src="https://github.com/user-attachments/assets/aa820558-8ed7-4a71-be2a-50fac8c6eca3" />

---

### 4.3 Ambil Items

```bash
curl.exe -X GET "http://127.0.0.1:8000/items" -H "accept: application/json"
```
<img width="1633" height="153" alt="Image" src="https://github.com/user-attachments/assets/ffc30554-f1ff-47ff-9412-1c77638589ad" />

---

### 4.4 Update Profil

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
<img width="1631" height="332" alt="Image" src="https://github.com/user-attachments/assets/956427e4-907f-4404-a5a3-4fba05d3bb9f" />

**Gagal (tanpa token):**
```bash
curl -Method PUT "http://127.0.0.1:8000/profile" `
  -Headers @{ 
      "accept" = "application/json"; 
      "Content-Type" = "application/json"
  } `
  -Body '{"name": "Ferdayy", "email": "user1@example.com"}'
```
<img width="1627" height="74" alt="Image" src="https://github.com/user-attachments/assets/d44e3ec9-99bd-4e64-8474-4e9e883fb259" />

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
<img width="1619" height="95" alt="Image" src="https://github.com/user-attachments/assets/89f4daa0-d1ff-48a5-895f-c72a461ede1a" />

---

## 5. Catatan & Asumsi

- Database **harus dibuat terlebih dahulu** sebelum menjalankan server, atau script `seed.py` akan gagal.
- `JWT_SECRET` **wajib diubah** menjadi string acak yang kuat sebelum digunakan di production.
- Saat **email user diubah**, token lama otomatis tidak valid dan diganti dengan token baru.
- Endpoint `/profile` memerlukan **Bearer token** yang valid pada header.
- Pada `PUT /profile`, minimal salah satu field (`name` atau `email`) harus diisi.

---

## 🧾 Lisensi

Proyek ini dibuat untuk kebutuhan tugas mata kuliah Integrasi Aplikasi Enterprise SI-47-06 Kelompok 7.
<br>
**Link Google Drive:** https://drive.google.com/drive/folders/1DlmoI4b2otan3toS3GxawvVh9_3ZnxBh?usp=sharing
<br>
Struktur Proyek:
<br>
<img width="363" height="614" alt="Image" src="https://github.com/user-attachments/assets/a8e2f435-db5f-4ed2-b90c-155e09ecdee6" />

📌 **Author:**
1. Ferdiansyah Adi Saputra (102022330113)
2. Kennteh Bryan (102022330093)
3. Syarief Saleh Madhy (102022300201)
4. I Gusti Ngurah Raja Putra Bumi (102022300159)
