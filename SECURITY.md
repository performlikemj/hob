# Security Checklist for Azure Deployment

This document outlines security best practices and configurations for the Afrikoop project on Azure.

## 🔒 Pre-Deployment Security

### Secrets Management

- [ ] **Generate strong Django SECRET_KEY** (min 50 characters)
  ```bash
  python3 -c "import secrets; print(secrets.token_urlsafe(50))"
  ```
- [ ] **Generate strong admin password** (min 16 characters, alphanumeric + symbols)
- [ ] **Never commit secrets to Git** (check `.gitignore` includes `.env`, `*.key`, `secrets.json`)
- [ ] **Use environment variables** for all secrets (no hardcoded values in code)
- [ ] **Audit codebase** for accidentally committed secrets:
  ```bash
  git log --all --full-history -- "*.env*" "*.key" "*.pem"
  ```

### Code Security

- [ ] **Ensure `DEBUG=False`** in production settings
- [ ] **Set specific `ALLOWED_HOSTS`** (not `*`)
- [ ] **Set specific `CSRF_TRUSTED_ORIGINS`** (HTTPS URLs only)
- [ ] **Review dependencies** for known vulnerabilities:
  ```bash
  pip install safety
  safety check -r requirements.txt
  ```
- [ ] **Pin dependency versions** in `requirements.txt` (no `>=` or `~=`)
- [ ] **Remove unused dependencies**

## 🌐 Network Security

### HTTPS/TLS

- [ ] **Enforce HTTPS** (`SECURE_SSL_REDIRECT=True`)
- [ ] **Enable HSTS** after testing (uncomment in `settings_prod.py`):
  ```python
  SECURE_HSTS_SECONDS = 31536000
  SECURE_HSTS_INCLUDE_SUBDOMAINS = True
  SECURE_HSTS_PRELOAD = True
  ```
- [ ] **Verify SSL certificate** is valid (Azure provides free managed certs)
- [ ] **Disable TLS 1.0/1.1** (Azure App Service defaults to TLS 1.2+)

### CORS Configuration

- [ ] **Set `FRONTEND_URL`** to exact frontend domain (no wildcards)
- [ ] **Verify `CORS_ALLOWED_ORIGINS`** contains only your frontend
- [ ] **Enable `CORS_ALLOW_CREDENTIALS=True`** only if using cookies
- [ ] **Test CORS** from frontend (should work) and other origins (should fail)

### Firewall Rules

- [ ] **Restrict admin panel access** (Azure App Service → Networking → Access Restrictions):
  - Add IP allowlist for admin routes (`/admin/*`)
  - Or use Azure Front Door with WAF
- [ ] **Block direct access to sensitive endpoints** (if using Azure Front Door)
- [ ] **Configure PostgreSQL firewall** (if using managed DB):
  - Allow only Azure services (0.0.0.0)
  - Add your office/home IP for direct DB access
  - Never allow 0.0.0.0/0 for production

## 🔐 Authentication & Authorization

### Django Admin

- [ ] **Change admin URL** from `/admin/` to something obscure (e.g., `/secret-admin-portal/`)
  ```python
  # urls.py
  path('secret-admin-portal/', admin.site.urls),
  ```
- [ ] **Require strong passwords** (already configured in `settings.py`)
- [ ] **Enable 2FA** for admin users (install `django-otp` or `django-two-factor-auth`)
- [ ] **Limit login attempts** (install `django-axes` or `django-defender`)
- [ ] **Review admin user permissions** (least privilege principle)
- [ ] **Disable admin for non-staff** (`is_staff=False` for regular users)

### API Authentication

- [ ] **Use token authentication** (already implemented)
- [ ] **Set token expiry** (optional, requires custom logic or `djangorestframework-simplejwt`)
- [ ] **Rotate tokens on password change**
- [ ] **Implement rate limiting** (install `django-ratelimit` or use Azure API Management)
- [ ] **Log failed authentication attempts**

## 🗄️ Database Security

### SQLite (Free Tier)

- [ ] **Verify database is on persistent storage** (`/home/site/db.sqlite3`)
- [ ] **Set up regular backups**:
  ```bash
  # Add to cron or Azure Logic App
  az webapp ssh --name app-afrikoop-backend-prod --resource-group rg-afrikoop-prod
  cd /home/site
  tar -czf db-backup-$(date +%Y%m%d).tar.gz db.sqlite3 media/
  # Upload to Azure Storage
  ```
- [ ] **Restrict file permissions** (App Service handles this)
- [ ] **Never expose database file** in static/media URLs

### PostgreSQL (Optional)

- [ ] **Use strong password** for admin user (min 16 chars)
- [ ] **Enable SSL** (`sslmode=require` in connection string)
- [ ] **Configure firewall rules** (see Network Security above)
- [ ] **Enable automatic backups** (7-day retention minimum)
- [ ] **Test backup restoration** (at least once)
- [ ] **Encrypt data at rest** (enabled by default on Azure)
- [ ] **Monitor connection logs** (enable via Azure Monitor)
- [ ] **Use managed identity** for DB access (advanced, optional)

## 🛡️ Application Security

### Input Validation

- [ ] **Django ORM parameterized queries** (already default)
- [ ] **Validate all user input** (forms, APIs)
- [ ] **Sanitize file uploads** (check file types, max size)
- [ ] **Limit upload size** (configure in `settings.py`):
  ```python
  DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
  FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
  ```
- [ ] **Validate image uploads** (Pillow already validates)

### XSS Protection

- [ ] **Use Django templates** (auto-escapes by default)
- [ ] **Never use `mark_safe()` with user input**
- [ ] **Set Content-Security-Policy header** (frontend `staticwebapp.config.json`):
  ```json
  "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
  ```
- [ ] **Enable XSS filter** (`X-XSS-Protection: 1; mode=block`, already set)

### CSRF Protection

- [ ] **CSRF middleware enabled** (already in `MIDDLEWARE`)
- [ ] **Use `@csrf_exempt` only for token-authenticated APIs** (already done)
- [ ] **Set `CSRF_COOKIE_SECURE=True`** (already in `settings_prod.py`)
- [ ] **Set `CSRF_COOKIE_SAMESITE='Lax'`** (already in `settings_prod.py`)

### Clickjacking Protection

- [ ] **Set `X-Frame-Options: DENY`** (already in `settings_prod.py`)
- [ ] **Or use CSP `frame-ancestors 'none'`** (stricter)

### Content Type Sniffing

- [ ] **Set `X-Content-Type-Options: nosniff`** (already in frontend config)

## 📝 Logging & Monitoring

### Application Logs

- [ ] **Enable detailed logging** (already configured in `settings_prod.py`)
- [ ] **Log authentication events** (logins, logouts, failed attempts)
- [ ] **Log admin actions** (Django admin logs by default)
- [ ] **Never log sensitive data** (passwords, tokens, credit cards)
- [ ] **Set log retention** (7-30 days for compliance)

### Azure Monitoring

- [ ] **Enable App Service diagnostics**:
  ```bash
  az webapp log config \
    --name app-afrikoop-backend-prod \
    --resource-group rg-afrikoop-prod \
    --application-logging filesystem \
    --level information
  ```
- [ ] **Set up alerts** (high CPU, errors, failed requests)
- [ ] **Monitor unusual traffic patterns** (sudden spikes, DDoS attempts)
- [ ] **Enable Application Insights** (optional, ~$2-10/mo):
  ```bash
  az monitor app-insights component create \
    --app appi-afrikoop-prod \
    --location eastus \
    --resource-group rg-afrikoop-prod
  ```

### Security Monitoring

- [ ] **Enable Azure Security Center** (free tier available)
- [ ] **Review security recommendations** monthly
- [ ] **Set up alerts for**:
  - Failed login attempts (>10 in 5 min)
  - Admin panel access from new IPs
  - Database connection errors
  - High error rates (5xx responses)

## 🔄 Operational Security

### Backup & Recovery

- [ ] **Backup database** (daily for SQLite, automatic for PostgreSQL)
- [ ] **Backup media files** (weekly, store in Azure Blob Storage)
- [ ] **Test restoration** (quarterly)
- [ ] **Document recovery procedure** (RTO: 4 hours, RPO: 24 hours)

### Patching & Updates

- [ ] **Update dependencies** monthly:
  ```bash
  pip list --outdated
  npm outdated
  ```
- [ ] **Apply security patches** immediately (CVEs)
- [ ] **Test updates in staging** before production
- [ ] **Subscribe to security advisories**:
  - Django: https://www.djangoproject.com/weblog/
  - React: https://github.com/facebook/react/security/advisories
  - Azure: https://azure.microsoft.com/en-us/updates/

### Access Control

- [ ] **Use separate accounts** (admin, developer, deploy)
- [ ] **Principle of least privilege** (minimal permissions)
- [ ] **Review access quarterly** (remove unused accounts)
- [ ] **Use Azure RBAC** for resource management
- [ ] **Enable MFA** for Azure account (https://aka.ms/mfasetup)

### Incident Response

- [ ] **Document incident response plan**:
  1. Detect: Monitor alerts, logs
  2. Contain: Isolate affected systems
  3. Eradicate: Remove threat
  4. Recover: Restore from backup
  5. Post-mortem: Document lessons learned
- [ ] **Assign on-call contact** (email, phone)
- [ ] **Test incident response** (tabletop exercise)

## 🧪 Security Testing

### Pre-Deployment Tests

- [ ] **Run Django security checks**:
  ```bash
  python manage.py check --deploy --settings=afrikoop.settings_prod
  ```
- [ ] **Test CORS** (from allowed and disallowed origins)
- [ ] **Test CSRF** (POST without token should fail)
- [ ] **Test authentication** (invalid tokens should fail)
- [ ] **Test rate limiting** (if implemented)
- [ ] **Verify HTTPS redirect** (HTTP should redirect to HTTPS)

### Post-Deployment Audits

- [ ] **Run OWASP ZAP** or similar (basic scan)
- [ ] **Check SSL Labs** (https://www.ssllabs.com/ssltest/)
  - Target: A or A+ rating
- [ ] **Check Security Headers** (https://securityheaders.com/)
  - Target: A or A+ rating
- [ ] **Penetration test** (optional, hire security firm for critical apps)

### Continuous Security

- [ ] **Automated dependency scanning** (GitHub Dependabot or Snyk)
- [ ] **Automated security tests** in CI/CD (e.g., Bandit for Python)
- [ ] **Monthly security review** (logs, access, dependencies)

## 📋 Compliance (Optional)

If handling sensitive data (PII, payments, health):

- [ ] **Review GDPR requirements** (if serving EU users)
- [ ] **Review CCPA requirements** (if serving California users)
- [ ] **Implement data retention policy** (auto-delete old data)
- [ ] **Add privacy policy** (link in footer)
- [ ] **Add terms of service**
- [ ] **Implement cookie consent** (if using analytics)
- [ ] **Encrypt PII at rest and in transit**
- [ ] **Document data processing activities**

## 🚨 Known Risks & Mitigations

### Risk: SQLite Corruption (Free Tier)

**Likelihood**: Low  
**Impact**: High (data loss)  
**Mitigation**: 
- Daily backups to Azure Storage
- Monitor disk space (App Service Free: 1GB)
- Consider PostgreSQL for production

### Risk: CPU Minute Limit (Free Tier)

**Likelihood**: Medium  
**Impact**: Medium (downtime)  
**Mitigation**:
- Monitor CPU usage via Azure Portal
- Upgrade to Basic ($13/mo) if exceeded
- Optimize queries, cache static content

### Risk: Admin Panel Brute Force

**Likelihood**: Medium  
**Impact**: High (unauthorized access)  
**Mitigation**:
- Change admin URL
- IP allowlist
- Install django-axes (rate limiting)
- Enable 2FA

### Risk: DDoS Attack

**Likelihood**: Low  
**Impact**: High (unavailability)  
**Mitigation**:
- Azure DDoS Protection (basic included, standard costs extra)
- Rate limiting at App Service or Azure Front Door
- Monitor traffic patterns

## ✅ Security Sign-Off

Before going live, confirm:

- [ ] All items in this checklist reviewed
- [ ] Secrets are stored securely (not in code)
- [ ] HTTPS is enforced
- [ ] Admin panel is protected
- [ ] Backups are configured
- [ ] Monitoring is enabled
- [ ] Incident response plan documented
- [ ] Security testing completed

**Signed by**: _________________________  
**Date**: _________________________  
**Next review**: _________________________ (quarterly)

---

**Last Updated**: 2025-01-06  
**Reviewed by**: Security Team / Michael Jones

