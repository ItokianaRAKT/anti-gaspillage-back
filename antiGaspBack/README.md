# Anti-Gaspillage — Backend API

API REST pour une plateforme de réduction du gaspillage alimentaire. Permet aux utilisateurs de mettre en vente des produits proches de leur date de péremption, de les réserver et de laisser des avis.

---

## Stack & dépendances

- **Django 6** + **Django REST Framework**
- **PostgreSQL**
- **JWT** — `djangorestframework-simplejwt`
- **django-cors-headers**
- **django-filter**
- **Pillow** (gestion des images)
- **python-dotenv**
- **Gunicorn** (production)

---

## Installation

```bash
# 1. Cloner et se placer dans le projet
git clone https://github.com/ItokianaRAKT/anti-gaspillage-back.git
cd anti-gaspillage-back/antiGaspBack

# 2. Créer et activer le virtualenv
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
touch .env
# Remplir les valeurs dans .env

# 5. Appliquer les migrations
python manage.py migrate

# 6. Lancer le serveur
python manage.py runserver
```

### Variables d'environnement (`.env`)

```env

SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=anti_gaspillage
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

```
