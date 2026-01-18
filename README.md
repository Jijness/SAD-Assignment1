# ASSIGNMENT 01 - SOFTWARE ARCHITECTURE AND DESIGN
**Sinh viên:** Nguyễn Đăng Trường 
**Mã sinh viên:** B22DCCN881
**Lớp:** B22CNPM03

## 1. TỔNG QUAN
Hệ thống **Book Store Web System** được triển khai theo 3 kiến trúc phần mềm khác nhau để so sánh và đánh giá:
1.  **Monolithic Architecture**: Một khối thống nhất, dùng chung Database.
2.  **Clean Architecture**: Tách biệt logic nghiệp vụ (Use Cases) và giao diện/DB, tuân thủ Dependency Rule.
3.  **Microservices Architecture**: Tách thành 3 dịch vụ độc lập giao tiếp qua REST API.

---

## 2. CÀI ĐẶT CHUNG (PREREQUISITES)

### Yêu cầu hệ thống:
* Python 3.10+
* MySQL Server (XAMPP hoặc MySQL Workbench)

### Bước 1: Clone và Cài đặt thư viện
```bash
git clone [https://github.com/Jijness/SAD-Assignment1.git](https://github.com/Jijness/SAD-Assignment1.git)
cd SAD-Assignment1

# Tạo môi trường ảo
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### Bước 2: Khởi tạo Database (MySQL)
Chạy các lệnh SQL sau trong MySQL Workbench để tạo 5 database cần thiết:
```sql
-- Database cho Monolithic
CREATE DATABASE bookstore_monolith CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
```sql
-- Database cho Clean Architecture
CREATE DATABASE bookstore_clean CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
```sql
-- Databases cho Microservices
CREATE DATABASE micro_book CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE micro_customer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE micro_cart CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 3. HƯỚNG DẪN CHẠY TỪNG HỆ THỐNG
### A. PHIÊN BẢN MONOLITHIC
Kiến trúc: MVT (Model-View-Template).

Luồng chạy: Browser -> View (Controller) -> Model (Database) -> Template (HTML).

Cách chạy:
```bash
cd monolith
# Setup DB (lần đầu)
python manage.py migrate
python manage.py createsuperuser
# Chạy Server
python manage.py runserver
```
* Truy cập: http://127.0.0.1:8000/
* Chức năng: Xem sách, Đăng ký/Đăng nhập, Giỏ hàng (Full UI).

### B. PHIÊN BẢN CLEAN ARCHITECTURE
Kiến trúc: Phân lớp hình củ hành (Onion).

Luồng chạy: 
1. View (Framework): Nhận request từ người dùng.
2. Use Case (Application): Xử lý logic nghiệp vụ (không cần biết DB/Web là gì).
3. Repository Interface (Domain): Định nghĩa hợp đồng giao tiếp.
4. Infrastructure (Data): Thực thi Interface, dùng Django ORM chọc vào DB.

Cách chạy:
```bash
cd clean_art
# Setup DB (lần đầu)
python manage.py migrate
python manage.py createsuperuser
# Chạy Server
python manage.py runserver
```
* Truy cập: http://127.0.0.1:8000/
* Chức năng: Xem sách, Đăng ký/Đăng nhập, Giỏ hàng (Full UI).

### C. PHIÊN BẢN MICROSERVICES
Kiến trúc: 3 Services độc lập, mỗi service có Database riêng, giao tiếp qua HTTP Requests.

Sơ đồ luồng dữ liệu (Data Flow):
1. Customer Service (8002): Quản lý User (Register/Login).
2. Book Service (8001): Quản lý kho sách.
3. Cart Service (8003):
    * Khi User thêm sách -> Gọi API sang Book Service để lấy giá tiền hiện tại.
    * Lưu vào DB riêng (micro_cart).

Cách chạy (Cần mở 3 Terminals):
```bash
cd micro/book
python manage.py migrate
python manage.py runserver 8001
```
```bash
cd micro/customer
python manage.py migrate
python manage.py runserver 8002
```
```bash
cd micro/cart
python manage.py migrate
python manage.py runserver 8003
```

Test với Postman:
* Get Books: GET http://127.0.0.1:8001/api/books/
* Register: POST http://127.0.0.1:8002/api/register/ (Body JSON: username, password)
* Add to Cart: POST http://127.0.0.1:8003/api/cart/add/
    * Body: {"user_id": 1, "book_id": 1}
    * Lưu ý: Cart Service sẽ tự động gọi Book Service để lấy giá.
