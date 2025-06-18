# Static Images Directory

This directory contains all static images used throughout the Sumi Jewelry Store website.

## Directory Structure

```
static/images/
├── logo.png           # Store logo
├── banner.jpg         # Home page banner
└── icons/            # Additional icons
```

## Image Requirements

### Logo (logo.png)
- Format: PNG with transparent background
- Size: 200x40 pixels
- Purpose: Used in the navigation bar
- Location: `static/images/logo.png`

### Banner (banner.jpg)
- Format: JPG
- Size: 1920x600 pixels
- Purpose: Home page hero section background
- Location: `static/images/banner.jpg`

### Icons
- Format: SVG or PNG
- Size: 32x32 or 64x64 pixels
- Purpose: Various UI elements
- Location: `static/images/icons/`

## Image Guidelines

1. **File Formats**
   - Use PNG for images that need transparency (logo, icons)
   - Use JPG for photographs and complex images (banner)
   - Use SVG for scalable icons when possible

2. **Optimization**
   - Compress all images before adding them
   - Keep file sizes under 200KB
   - Use tools like TinyPNG or ImageOptim for compression

3. **Naming Convention**
   - Use lowercase letters
   - Use hyphens (-) instead of spaces
   - Be descriptive (e.g., `facebook-icon.png`, `instagram-icon.png`)

4. **After Adding Images**
   - Run `python manage.py collectstatic` to update static files
   - Restart the Django development server

## Adding New Images

1. Place your image in the appropriate directory
2. Follow the naming convention
3. Optimize the image
4. Run collectstatic command
5. Test the image in the browser 