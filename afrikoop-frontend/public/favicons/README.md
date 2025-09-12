Place favicon and app icon files in this folder. Files here are served statically by Vite at the site root.

Common files
- favicon.ico (16/32/48px multi-res)
- favicon.png (at least 32x32)
- favicon.svg (preferred for modern browsers)
- apple-touch-icon.png (180x180)
- site.webmanifest (PWA metadata)

Referencing in index.html
<link rel="icon" href="/favicons/favicon.svg" type="image/svg+xml" />
<link rel="icon" href="/favicons/favicon.png" sizes="32x32" />
<link rel="apple-touch-icon" href="/favicons/apple-touch-icon.png" />

