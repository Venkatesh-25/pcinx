# Deployment Guide

## 🚀 FRA Atlas MVP Deployment Guide

This comprehensive guide covers all deployment options for the FRA Atlas MVP, from simple static hosting to enterprise-level production environments.

### 🎯 Deployment Overview

The FRA Atlas MVP is designed with **zero-dependency architecture**, making it incredibly easy to deploy across various platforms and environments. No build process, no server-side requirements - just pure web technologies that work anywhere.

### 📋 Prerequisites

#### **Basic Requirements**
- **Web Server**: Any HTTP server (Apache, Nginx, IIS, or static hosting)
- **Browser Support**: Modern browsers (Chrome 80+, Firefox 75+, Edge 80+, Safari 13+)
- **Internet Connection**: Required for map tiles and external CDN resources
- **HTTPS**: Recommended for production (required for some browser features)

#### **Optional Requirements**
- **Custom Domain**: For branded access
- **SSL Certificate**: For HTTPS security
- **CDN**: For global performance optimization
- **Analytics**: For usage tracking and monitoring

### 🌐 Deployment Options

#### **Option 1: GitHub Pages (Recommended for Demo)**

##### **Automatic Deployment** ✅ *Already Configured*
Your repository is already set up with GitHub Pages:

- **Live URL**: https://ultrabot05.github.io/fra-atlas-mvp/
- **Auto-deploy**: Every push to master branch triggers deployment
- **Zero Cost**: Free hosting for public repositories
- **Global CDN**: GitHub's worldwide content delivery network

##### **Manual GitHub Pages Setup** (if needed)
```bash
# 1. Ensure your code is in master branch
git checkout master
git push origin master

# 2. Enable GitHub Pages via GitHub CLI
gh api repos/UltraBot05/fra-atlas-mvp/pages -X POST \
  -f "source[branch]=master" -f "source[path]=/"

# 3. Verify deployment
gh api repos/UltraBot05/fra-atlas-mvp/pages
```

##### **Custom Domain Setup**
```bash
# 1. Add CNAME file to repository root
echo "yourdomain.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push origin master

# 2. Configure DNS records at your domain provider
# Add CNAME record: www.yourdomain.com -> ultrabot05.github.io
# Add A records for apex domain:
# 185.199.108.153
# 185.199.109.153
# 185.199.110.153
# 185.199.111.153
```

#### **Option 2: Netlify (Recommended for Production)**

##### **Deploy from Git** (Automated)
```bash
# 1. Connect GitHub repository to Netlify
# - Go to https://netlify.com
# - Click "New site from Git"
# - Choose GitHub and select fra-atlas-mvp repository

# 2. Build settings
Build command: (leave empty - no build needed)
Publish directory: . (root directory)
Production branch: master

# 3. Deploy settings
# - Auto-deploy: ON
# - HTTPS: Enable
# - Custom domain: Configure if needed
```

##### **Manual Deploy** (Drag & Drop)
```bash
# 1. Download repository as ZIP or clone locally
git clone https://github.com/UltraBot05/fra-atlas-mvp.git
cd fra-atlas-mvp

# 2. Drag and drop entire folder to Netlify deploy area
# OR zip the contents and upload

# 3. Get deployment URL
# Netlify provides instant HTTPS URL like: https://amazing-name-123456.netlify.app
```

##### **Advanced Netlify Configuration**
Create `netlify.toml` in repository root:
```toml
[build]
  publish = "."
  
[build.environment]
  NODE_VERSION = "18"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "*.css"
  [headers.values]
    Cache-Control = "max-age=31536000"

[[headers]]
  for = "*.js"
  [headers.values]
    Cache-Control = "max-age=31536000"

[[headers]]
  for = "*.geojson"
  [headers.values]
    Cache-Control = "max-age=3600"
    Content-Type = "application/geo+json"

[[redirects]]
  from = "/api/*"
  to = "https://api.fra-atlas.gov.in/:splat"
  status = 200
  force = true
  condition = "Country=IN"
```

#### **Option 3: Vercel (Developer-Friendly)**

##### **CLI Deployment**
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy from project directory
cd fra-atlas-mvp
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Link to existing project? No
# - Project name: fra-atlas-mvp
# - Directory: ./
# - Override settings? No

# 3. Custom domain (optional)
vercel --prod
vercel domains add yourdomain.com
```

##### **GitHub Integration**
```bash
# 1. Import project from GitHub
# - Go to https://vercel.com/dashboard
# - Click "Import Project"
# - Select GitHub repository

# 2. Configure project
Framework Preset: Other
Build Command: (leave empty)
Output Directory: ./
Install Command: (leave empty)

# 3. Deploy
# Automatic deployment on every git push
```

#### **Option 4: Apache Web Server**

##### **Ubuntu/Debian Setup**
```bash
# 1. Install Apache
sudo apt update
sudo apt install apache2

# 2. Clone repository to web directory
sudo git clone https://github.com/UltraBot05/fra-atlas-mvp.git /var/www/fra-atlas

# 3. Set permissions
sudo chown -R www-data:www-data /var/www/fra-atlas
sudo chmod -R 755 /var/www/fra-atlas

# 4. Create virtual host
sudo nano /etc/apache2/sites-available/fra-atlas.conf
```

**Apache Virtual Host Configuration:**
```apache
<VirtualHost *:80>
    ServerName fra-atlas.yourdomain.com
    DocumentRoot /var/www/fra-atlas
    DirectoryIndex index.html
    
    <Directory /var/www/fra-atlas>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
        
        # Enable compression
        <IfModule mod_deflate.c>
            AddOutputFilterByType DEFLATE text/plain
            AddOutputFilterByType DEFLATE text/html
            AddOutputFilterByType DEFLATE text/xml
            AddOutputFilterByType DEFLATE text/css
            AddOutputFilterByType DEFLATE application/xml
            AddOutputFilterByType DEFLATE application/xhtml+xml
            AddOutputFilterByType DEFLATE application/rss+xml
            AddOutputFilterByType DEFLATE application/javascript
            AddOutputFilterByType DEFLATE application/x-javascript
            AddOutputFilterByType DEFLATE application/json
            AddOutputFilterByType DEFLATE application/geo+json
        </IfModule>
        
        # Set cache headers
        <IfModule mod_expires.c>
            ExpiresActive On
            ExpiresByType text/css "access plus 1 year"
            ExpiresByType application/javascript "access plus 1 year"
            ExpiresByType application/geo+json "access plus 1 hour"
            ExpiresByType text/html "access plus 1 hour"
        </IfModule>
    </Directory>
    
    # Redirect to HTTPS
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
</VirtualHost>

<VirtualHost *:443>
    ServerName fra-atlas.yourdomain.com
    DocumentRoot /var/www/fra-atlas
    DirectoryIndex index.html
    
    SSLEngine on
    SSLCertificateFile /path/to/certificate.crt
    SSLCertificateKeyFile /path/to/private.key
    
    # Include same directory configuration as above
</VirtualHost>
```

```bash
# 5. Enable site and modules
sudo a2ensite fra-atlas.conf
sudo a2enmod rewrite
sudo a2enmod deflate
sudo a2enmod expires
sudo a2enmod ssl

# 6. Restart Apache
sudo systemctl restart apache2
```

#### **Option 5: Nginx**

##### **Configuration File**
```nginx
server {
    listen 80;
    server_name fra-atlas.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name fra-atlas.yourdomain.com;
    
    root /var/www/fra-atlas;
    index index.html;
    
    # SSL Configuration
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate max-age=0;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json application/geo+json;
    
    # Cache static assets
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Cache GeoJSON data
    location ~* \.geojson$ {
        expires 1h;
        add_header Cache-Control "public";
        add_header Content-Type "application/geo+json";
    }
    
    # Main application
    location / {
        try_files $uri $uri/ /index.html;
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

#### **Option 6: Docker Deployment**

##### **Dockerfile**
```dockerfile
FROM nginx:alpine

# Copy application files
COPY . /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set permissions
RUN chmod -R 755 /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

##### **Docker Compose**
```yaml
version: '3.8'

services:
  fra-atlas:
    build: .
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./ssl:/etc/nginx/ssl:ro
    environment:
      - NGINX_HOST=fra-atlas.yourdomain.com
      - NGINX_PORT=80
    restart: unless-stopped
    
  # Optional: Add SSL certificate renewal
  certbot:
    image: certbot/certbot
    volumes:
      - ./ssl:/etc/letsencrypt
      - ./certbot-var:/var/lib/letsencrypt
    command: renew --quiet
    depends_on:
      - fra-atlas
```

##### **Deployment Commands**
```bash
# 1. Build and run
docker-compose up -d

# 2. Update deployment
git pull origin master
docker-compose build
docker-compose up -d

# 3. View logs
docker-compose logs -f fra-atlas

# 4. Scale (if needed)
docker-compose up -d --scale fra-atlas=3
```

### 🔧 Environment-Specific Configurations

#### **Development Environment**
```javascript
// config/development.js
const config = {
    api_base_url: 'http://localhost:3000/api',
    map_debug: true,
    enable_analytics: false,
    cache_duration: 0,
    log_level: 'debug'
};
```

#### **Staging Environment**
```javascript
// config/staging.js
const config = {
    api_base_url: 'https://staging-api.fra-atlas.gov.in/api',
    map_debug: false,
    enable_analytics: true,
    cache_duration: 300, // 5 minutes
    log_level: 'info'
};
```

#### **Production Environment**
```javascript
// config/production.js
const config = {
    api_base_url: 'https://api.fra-atlas.gov.in/api',
    map_debug: false,
    enable_analytics: true,
    cache_duration: 3600, // 1 hour
    log_level: 'error',
    enable_pwa: true
};
```

### 🔒 Security Considerations

#### **HTTPS Configuration**
```bash
# Let's Encrypt SSL Certificate (Free)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d fra-atlas.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### **Security Headers**
```nginx
# Additional security headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

#### **Content Security Policy**
```html
<!-- Add to index.html head section -->
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' 'unsafe-inline' https://unpkg.com https://cdnjs.cloudflare.com;
    style-src 'self' 'unsafe-inline' https://unpkg.com https://cdnjs.cloudflare.com;
    img-src 'self' data: https: blob:;
    connect-src 'self' https:;
    font-src 'self' https://cdnjs.cloudflare.com;
    frame-src 'none';
">
```

### 📊 Performance Optimization

#### **CDN Configuration**
```javascript
// Update external resource URLs for CDN
const CDN_CONFIG = {
    leaflet: 'https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/',
    fontawesome: 'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.0.0/css/'
};
```

#### **Service Worker for Caching**
```javascript
// sw.js - Service Worker for offline capability
const CACHE_NAME = 'fra-atlas-v1.0.0';
const urlsToCache = [
    '/',
    '/index.html',
    '/css/main.css',
    '/css/dashboard.css',
    '/css/modal.css',
    '/css/map.css',
    '/js/app.js',
    '/js/components/map-manager.js',
    '/js/components/dashboard.js',
    '/js/components/report-modal.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
    );
});
```

### 📈 Monitoring and Analytics

#### **Google Analytics Integration**
```html
<!-- Add to index.html head section -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

#### **Server Monitoring**
```bash
# Install monitoring tools
sudo apt install htop iotop netstat

# Monitor web server
sudo systemctl status nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Monitor system resources
htop
df -h
free -m
```

### 🔄 CI/CD Pipeline

#### **GitHub Actions Deployment**
```yaml
# .github/workflows/deploy.yml
name: Deploy FRA Atlas MVP

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Run tests
      run: |
        # Add test commands when implemented
        echo "Tests would run here"
    
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/master'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
    
    - name: Deploy to Production
      if: github.ref == 'refs/heads/master'
      run: |
        # Add production deployment commands
        echo "Production deployment would run here"
```

### 🆘 Troubleshooting

#### **Common Deployment Issues**

##### **Map Tiles Not Loading**
```bash
# Check CORS headers
curl -I https://your-domain.com
# Should include: Access-Control-Allow-Origin: *

# Check network connectivity
ping a.tile.openstreetmap.org
```

##### **JavaScript Errors**
```bash
# Check browser console
# F12 -> Console tab
# Look for CORS, CSP, or loading errors

# Check file permissions
ls -la /var/www/fra-atlas/
# Should be readable by web server user
```

##### **Performance Issues**
```bash
# Enable compression
# Check server configuration for gzip/deflate

# Optimize images
# Use WebP format where possible
# Compress PNG/JPEG files

# Check CDN configuration
# Verify external resources load quickly
```

### 📞 Support and Maintenance

#### **Regular Maintenance Tasks**
- **Weekly**: Check server logs and performance metrics
- **Monthly**: Update SSL certificates and security patches
- **Quarterly**: Review and update dependencies
- **Annually**: Security audit and performance review

#### **Backup Strategy**
```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/backup/fra-atlas"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
tar -czf "$BACKUP_DIR/fra-atlas-$DATE.tar.gz" /var/www/fra-atlas/

# Keep only last 30 days
find $BACKUP_DIR -name "fra-atlas-*.tar.gz" -mtime +30 -delete
```

---

**Your FRA Atlas MVP is now ready for deployment across any environment - from simple GitHub Pages to enterprise production servers! 🚀🌿**