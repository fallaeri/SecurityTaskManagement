#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  SecureTask — Windows Compatible Setup Script
# ─────────────────────────────────────────────────────────────
set -e

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo -e "${BLUE}"
echo "  ███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗"
echo "  ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝"
echo "  ███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗  "
echo "  ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝  "
echo "  ███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗"
echo "  ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝"
echo -e "       Secure Task Management System${NC}"
echo ""

# 1. Create venv
echo -e "${YELLOW}[1/5] Creating venv...${NC}"
python -m venv venv

# safe activation (Git Bash)
if [ -f venv/Scripts/activate ]; then
  source venv/Scripts/activate
else
  echo "ERROR: venv activation failed"
  exit 1
fi

echo -e "${GREEN}✓ venv ready${NC}"

# 2. Upgrade tools
echo -e "${YELLOW}[2/5] Installing dependencies...${NC}"
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

echo -e "${GREEN}✓ packages installed${NC}"

# 3. .env setup
echo -e "${YELLOW}[3/5] Setting env...${NC}"

if [ ! -f .env ]; then
  cp .env.example .env

  SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(50))")

  python -c "
from pathlib import Path
p = Path('.env')
p.write_text(p.read_text().replace(
'your-very-secret-key-change-this-to-something-random',
'$SECRET'
))
"

  echo "✓ .env created"
else
  echo "✓ .env exists"
fi

# 4. DB
echo -e "${YELLOW}[4/5] Migrations...${NC}"
python manage.py makemigrations
python manage.py migrate

echo -e "${GREEN}✓ DB ready${NC}"

# 5. Admin
echo -e "${YELLOW}[5/5] Create admin...${NC}"

python manage.py shell -c "
from django.contrib.auth.models import User
from user_app.models import UserProfile

u = input('Admin username [admin]: ') or 'admin'
e = input('Email [admin@example.com]: ') or 'admin@example.com'

if User.objects.filter(username=u).exists():
    print('User exists')
else:
    import getpass
    while True:
        p1 = getpass.getpass('Password (12+ chars): ')
        p2 = getpass.getpass('Confirm: ')
        if p1 == p2 and len(p1) >= 12:
            break
        print('Try again')

    user = User.objects.create_superuser(u, e, p1)
    UserProfile.objects.create(user=user, role='admin')
    print('Admin created')
"

echo ""
echo -e "${GREEN}DONE → python manage.py runserver${NC}"