# MANAGER CAMPAIGN API

Hệ thống Backend (**FastAPI**) quản lý Campaign. Cung cấp các API để quản lý người dùng, chiến dịch, thành viên chiến dịch và nhiệm vụ.

## Công nghệ sử dụng

* **Framework:** FastAPI
* **Database:** MySQL, SQLAlchemy (ORM)
* **Xác thực:** JWT (JSON Web Tokens), Bcrypt
* **Validation:** Pydantic
* **Môi trường ảo:** venv

---

## Hướng dẫn Cài đặt & Chạy dự án

### Bước 1: Tạo và kích hoạt môi trường ảo (Virtual Environment)

Mở Terminal tại thư mục gốc của dự án và chạy:

```powershell
python -m venv .venv
```

Kích hoạt môi trường ảo trên Windows:

```powershell
.\.venv\Scripts\activate
```

Nếu kích hoạt thành công, Terminal sẽ hiển thị:

```text
(.venv)
```

### Bước 2: Cài đặt thư viện

Sau khi kích hoạt môi trường ảo, chạy:

```powershell
pip install -r requirements.txt
```

### Bước 3: Cấu hình cơ sở dữ liệu (Database)

1. Mở MySQL và tạo database:

```sql
CREATE DATABASE campaign_management_db;
```

2. Copy file `.env.example` thành file mới có tên `.env`.

3. Mở file `.env` và thay đổi thông tin `DATABASE_URL` theo tài khoản MySQL trên máy của bạn.

Ví dụ:

```env
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/campaign_management_db

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Trong đó:

* `root`: username MySQL.
* `123456`: password MySQL.
* `campaign_management_db`: tên database.

> Không chia sẻ hoặc commit file `.env` lên GitHub vì file này chứa thông tin cấu hình bảo mật.

### Bước 4: Khởi động Server

Chạy lệnh:

```powershell
uvicorn app.main:app --reload
```

Nếu khởi động thành công, Terminal sẽ hiển thị:

```text
Uvicorn running on http://127.0.0.1:8000
```

Hệ thống sẽ tự động khởi tạo các bảng trong database nếu chưa tồn tại.

### Bước 5: Kiểm tra và sử dụng
* **Swagger UI (Tài liệu API tự động):** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

