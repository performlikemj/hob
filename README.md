# Afrikoop Project

House of Bijou community website with Django backend and React frontend.

## Project Structure

```
afrikoop_project/
├── afrikoop-backend/       # Django REST API
│   ├── core/              # Main app (models, views, admin)
│   ├── afrikoop/          # Project settings
│   ├── startup.sh         # Azure App Service startup script
│   └── manage.py
├── afrikoop-frontend/      # React SPA (Vite + Tailwind)
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── contexts/      # Auth context
│   │   └── locales/       # i18n translations
│   └── staticwebapp.config.json
├── infra/                  # Azure Bicep templates
│   ├── main.bicep
│   └── main.parameters.json
├── .github/workflows/      # CI/CD pipelines
│   ├── deploy-backend.yml
│   └── deploy-frontend.yml
├── deploy.sh               # Manual deployment script
├── AZURE_DEPLOYMENT.md     # Detailed deployment guide
└── requirements.txt        # Python dependencies
```

## Features

- **Mission Page**: Bilingual (EN/JA) mission statement with hero image
- **Cleaning Service**: Service description, features, gallery, contact form
- **Events**: Event listing with registration (requires auth)
- **User Auth**: Token-based authentication (register, login, logout)
- **Contact Form**: Simple inquiry form stored in database
- **Admin Panel**: Django admin with Jazzmin theme for content management
- **i18n**: Full internationalization support (English & Japanese)

## Local Development

### Backend

```bash
cd afrikoop-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://localhost:8000/admin/

### Frontend

```bash
cd afrikoop-frontend
npm install
npm run dev
```

Visit: http://localhost:3000

## Azure Deployment

See **[AZURE_DEPLOYMENT.md](./AZURE_DEPLOYMENT.md)** for complete deployment guide.

### Quick Deploy (Manual)

```bash
# Login to Azure
az login
az account set --subscription 63ceeeac-fe3f-4bcb-b6d2-b7aa7fd6bf52

# Deploy infrastructure and backend
./deploy.sh

# Deploy frontend via GitHub Actions (see AZURE_DEPLOYMENT.md)
```

### Automated Deploy (GitHub Actions)

1. Set up GitHub Secrets (see AZURE_DEPLOYMENT.md Step 7)
2. Push to `main` branch
3. Workflows automatically deploy backend and frontend

## Architecture

- **Backend**: Azure App Service (Free tier, Python 3.11, Linux)
- **Frontend**: Azure Static Web Apps (Free tier)
- **Database**: SQLite on persistent storage (or optional PostgreSQL)
- **Storage**: Local `/home/site/media` (or optional Azure Blob Storage)
- **CI/CD**: GitHub Actions

## Cost Estimate

- **Free tier**: $0/mo (60 CPU min/day limit)
- **Basic tier**: ~$13-18/mo (no CPU limits)
- **With PostgreSQL**: ~$38-58/mo (adds $25-45/mo)

For $20/mo budget: Use Free tier with SQLite, monitor CPU usage.

## Security Features

✅ HTTPS only (enforced)  
✅ CORS restricted to frontend domain  
✅ CSRF protection enabled  
✅ Secure cookies (Secure, SameSite, HttpOnly)  
✅ HSTS (HTTP Strict Transport Security)  
✅ Content Security Policy headers  
✅ SQL injection protection (Django ORM)  
✅ XSS protection (React + Django templates)  
✅ Secrets in environment variables (no hardcoded keys)  
✅ Token-based API authentication  
✅ Password hashing (Django bcrypt)  

See **Security Checklist** in AZURE_DEPLOYMENT.md for full list.

## Environment Variables

### Backend (Django)

Required in production:

- `DJANGO_SECRET_KEY`: Strong random key (min 50 chars)
- `DJANGO_ALLOWED_HOSTS`: Comma-separated domains
- `FRONTEND_URL`: Frontend origin for CORS
- `ADMIN_EMAIL`: Admin user email
- `ADMIN_PASSWORD`: Admin user password

Optional:

- `AZURE_POSTGRESQL_HOST`: PostgreSQL host (omit to use SQLite)
- `AZURE_POSTGRESQL_NAME`: Database name
- `AZURE_POSTGRESQL_USER`: Database username
- `AZURE_POSTGRESQL_PASSWORD`: Database password

### Frontend (React)

- `VITE_API_URL`: Backend API URL (e.g., `https://app-afrikoop-backend-prod.azurewebsites.net/api`)

## API Endpoints

### Public Endpoints

- `GET /api/mission/` - Mission page content
- `GET /api/cleaning-service/` - Cleaning service page
- `GET /api/events/` - Event list (paginated)
- `GET /api/events-page/` - Events page settings
- `POST /api/contact/` - Contact form submission
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/i18n/{lang}/` - i18n translations

### Authenticated Endpoints

- `POST /api/events/{id}/register/` - Register for event (requires token)
- `POST /api/auth/logout/` - Logout (requires token)

All endpoints support `?lang=en` or `?lang=ja` query parameter for language-specific content.

## Database Models

- `MissionPage` - Mission statement (single record)
- `CleaningServicePage` - Cleaning service info
- `CleaningFeature` - Feature bullets
- `CleaningGalleryImage` - Gallery images
- `Event` - Events/volunteer opportunities
- `EventImage` - Event photos
- `EventRegistration` - User event sign-ups
- `EventsPageSettings` - Events page hero
- `ContactMessage` - Contact form submissions
- `User` - Django auth users
- `Token` - API auth tokens
- `TranslatableString` - UI string overrides
- `SiteTextSettings` - Site-wide text settings
- `VolunteerGroup` - Volunteer groups
- `VolunteerMembership` - User group memberships

## Technologies

### Backend

- Django 5.2
- Python 3.11
- Gunicorn (WSGI server)
- WhiteNoise (static file serving)
- django-cors-headers (CORS)
- django-jazzmin (admin theme)
- Pillow (image processing)

### Frontend

- React 18
- Vite (build tool)
- Tailwind CSS
- React Router
- Axios (HTTP client)
- i18next (internationalization)

### Infrastructure

- Azure App Service
- Azure Static Web Apps
- Azure Bicep (IaC)
- GitHub Actions (CI/CD)

## Support

For deployment issues, see [AZURE_DEPLOYMENT.md](./AZURE_DEPLOYMENT.md) troubleshooting section.

## License

Private project - all rights reserved.

---

**Maintained by**: Michael Jones  
**Last Updated**: 2025-01-06

