# Secure Task Management System

> Django web application demonstrating OWASP Top 10 security practices

---

## Features

| Feature        | Description                                                 |
| -------------- | ----------------------------------------------------------- |
| Authentication | Register, login, logout with Argon2 password hashing        |
| RBAC           | Admin sees all tasks + audit logs; Users see only their own |
| Task CRUD      | Create, read, update, delete tasks with priority and status |
| File Upload    | Secure upload with MIME validation, UUID rename, 5MB limit  |
| Audit Log      | Every login, logout, and action is logged with IP address   |
| Brute Force    | django-axes locks account after 5 failed login attempts     |
| CSRF           | All forms protected by CSRF tokens                          |
| XSS            | bleach sanitises all user input; Django auto-escaping on    |

---

### Option A — One-command setup (recommended)

```bash
git clone <your-repo-url>
cd secure_task_mgmt
bash setup.sh
```

That's it! The script creates the venv, installs packages, runs migrations, and creates your admin account.

Then start the server:

```bash
source venv/bin/activate   # Windows: venv\Scripts\activate
python manage.py runserver
```

Open → http://127.0.0.1:8000

---

### Option B — Manual step-by-step

```bash
# 1. Clone and enter folder
git clone <your-repo-url>
cd secure_task_mgmt

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Create your .env file
cp .env.example .env
# Edit .env and set a real SECRET_KEY

# 5. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create admin superuser
python manage.py createsuperuser
# Then set the admin role in Django Admin or shell:
python manage.py shell -c "
from django.contrib.auth.models import User
from user_app.models import UserProfile
u = User.objects.get(username='admin')  # change to your username
UserProfile.objects.get_or_create(u, role='admin')
"

# 7. Run!
python manage.py runserver
```

---

### Option C — Docker

```bash
cp .env.example .env
docker-compose up --build
```

Open → http://127.0.0.1:8000

---

## Default Accounts

After setup, you'll have the admin account you created.

To create a regular user account, go to `/auth/register/`.

| URL               | Description             |
| ----------------- | ----------------------- |
| `/` or `/tasks/`  | Dashboard (task list)   |
| `/auth/login/`    | Login                   |
| `/auth/register/` | Register new account    |
| `/profile/`       | User profile            |
| `/audit/`         | Audit logs (Admin only) |
| `/uploads/`       | File upload             |
| `/admin/`         | Django Admin panel      |

---

## OWASP Top 10 Mapping

| OWASP Risk                    | Mitigation in this project                                             |
| ----------------------------- | ---------------------------------------------------------------------- |
| A01 Broken Access Control     | RBAC on every view; IDOR prevented via `filter(owner=request.user)`    |
| A02 Cryptographic Failures    | Argon2 hashing; HttpOnly + SameSite cookies; secrets in `.env`         |
| A03 Injection                 | Django ORM only (no raw SQL); bleach sanitises all text input          |
| A04 Insecure Design           | Least privilege; UUID PKs prevent enumeration; files renamed on upload |
| A05 Security Misconfiguration | Custom 403/404 pages hide stack traces; security headers set           |
| A06 Vulnerable Components     | All dependencies pinned in `requirements.txt`; run `pip audit`         |
| A07 Auth & Session Failures   | django-axes lockout after 5 attempts; 30-min session timeout           |
| A08 Software & Data Integrity | CSRF protection on all POST forms                                      |
| A09 Logging Failures          | AuditLog records every action with user, IP, timestamp                 |
| A10 SSRF                      | No external URL fetching; file uploads validated by MIME type          |

---

## Security Settings Summary

```python
# settings.py highlights
PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher"]
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1800          # 30-minute timeout
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
AXES_FAILURE_LIMIT = 5             # Lock after 5 failed logins
AUTH_PASSWORD_VALIDATORS min_length = 12
```

---

## Testing Security Features

```bash
# Run all tests
python manage.py test

# Check for deployment security issues
python manage.py check --deploy

# Check for known CVEs in dependencies
pip install pip-audit
pip-audit
```

**Manual tests:**

1. Try logging in with wrong password 5 times → should be locked out
2. Log in as a User, visit `/audit/` → should see 403
3. Paste `<script>alert(1)</script>` in task title → should be escaped
4. Try uploading a `.exe` file → should be rejected
5. Try accessing `/tasks/<another-user-uuid>/` → should be 403

---

## Database Models

```
User (Django built-in)
 └── UserProfile (role: admin/user)

Task (UUID pk, owner FK, title, description, priority, status, due_date)
AuditLog (UUID pk, user FK, action, detail, ip_address, timestamp)
UploadedFile (UUID pk, owner FK, original_name, file, mime_type, file_size)
```

---
