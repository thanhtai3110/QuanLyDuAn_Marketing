# MANAGER CAMPAIGN API

Hệ thống Backend (FastAPI) quản lý Campaign. Cung cấp các API để quản lý người dùng, chiến dịch, thành viên và nhiệm vụ.

## Công nghệ sử dụng

* **Framework:** FastAPI
* **Database:** MySQL, SQLAlchemy (ORM)
* **Xác thực:** JWT (JSON Web Tokens), Bcrypt
* **Môi trường ảo:** venv

---

## Hướng dẫn Cài đặt & Chạy dự án

### Bước 1: Tạo và kích hoạt môi trường ảo

Mở Terminal tại thư mục gốc của dự án và chạy:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Bước 2: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình cơ sở dữ liệu

1. Mở MySQL và tạo database:

```sql
CREATE DATABASE campaign_management_db;
```

2. Copy file `.env.example` thành `.env`.
3. Mở `.env` và cấu hình thông tin:

```env
DATABASE_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Bước 4: Khởi động Server

Chạy lệnh:

```bash
uvicorn app.main:app --reload
```

Hệ thống sẽ tự động tạo các bảng trong Database nếu chưa có.

### Bước 5: Kiểm tra và sử dụng

* **API Health Check:** http://127.0.0.1:8000/health
* **Swagger UI:** http://127.0.0.1:8000/docs
* **ReDoc:** http://127.0.0.1:8000/redoc
