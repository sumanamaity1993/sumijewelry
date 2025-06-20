# Sumi Jewelry Store

A Django-based e-commerce platform for Sumi Jewelry.

## Local Development Setup

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Collect static files:
```bash
python manage.py collectstatic --noinput
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Django Management Commands

This project includes several custom Django management commands for data management and setup.

### Available Commands

#### Team Management
```bash
# Add default team members (CEO and Developer)
python manage.py add_team_members

# Remove all team members (requires confirmation)
python manage.py cleanup_team --confirm
```

#### Data Management
```bash
# Update product prices (if needed)
python manage.py update_prices
```

#### Data Backup/Restore
```bash
# Use the data management script for backups
python manage_data.py
```

### Command Details

- **`add_team_members`**: Creates default team members (Sumana Maity as CEO and Tapas as Developer)
- **`cleanup_team`**: Removes all team members from the database (use with caution)
- **`update_prices`**: Updates product prices (if price update logic is implemented)
- **`manage_data.py`**: Interactive script for database and media file backup/restore

### Safety Features
- The `cleanup_team` command requires the `--confirm` flag to prevent accidental deletion
- All commands provide clear feedback about what actions were performed
- Commands follow Django's standard output formatting

## Data Management Strategy

This project uses a **separate database and media management approach** optimized for free hosting platforms like PythonAnywhere.

### Database Management
- **Local Development**: Uses SQLite database (`db.sqlite3`) - ignored by git
- **Production**: Uses separate database on hosting platform
- **Sync Method**: Manual management through Django admin
- **Backup**: Download production database when needed for local testing

### Media Files Management
- **Product Images**: Tracked in git (in `media/` directory)
- **Automatic Sync**: Images are automatically deployed with code
- **Benefits**: Product images are version-controlled and always available

### Workflow
1. **Add products locally** → Test in Django admin
2. **Add same products in production** → Through production Django admin
3. **Upload images locally** → They sync automatically via git
4. **Download production data** → When needed for local testing

### Benefits of This Approach
✅ **Simple and reliable** - No complex sync processes
✅ **Free hosting compatible** - Works within PythonAnywhere free tier limits
✅ **Full control** - You decide when to sync data
✅ **No risk** - Can't accidentally overwrite production data
✅ **Cost-effective** - Perfect for 3-month free trial period

## Deployment to PythonAnywhere

1. Sign up for a PythonAnywhere account at https://www.pythonanywhere.com/

2. In PythonAnywhere dashboard:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python version (3.10 or newer)

3. Set up your virtual environment:
```bash
# In PythonAnywhere bash console
mkvirtualenv --python=/usr/bin/python3.10 sumi-jewelry
pip install -r requirements.txt
```

4. Upload your code:
   - Go to "Files" tab
   - Create a new directory (e.g., `sumi-jewelry`)
   - Upload your project files or clone from your repository
   - Make sure to include all files except `venv/`, `__pycache__/`, and `.git/`

5. Configure your web app:
   - Go to "Web" tab
   - Set "Source code" to your project directory
   - Set "Working directory" to your project directory
   - Set "WSGI configuration file" to your project's WSGI file
   - Update the WSGI file to point to your project:
```python
import os
import sys

path = '/home/YOUR_USERNAME/sumi-jewelry'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sumi_jewelry_store.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. Configure environment variables:
   - Go to "Web" tab
   - Add these to "Environment variables":
```
DJANGO_SETTINGS_MODULE=sumi_jewelry_store.settings
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-username.pythonanywhere.com
```

7. Set up static files:
   - Go to "Web" tab
   - Under "Static files", add:
     - URL: `/static/`
     - Directory: `/home/YOUR_USERNAME/sumi-jewelry/staticfiles`
   - Under "Static files", add:
     - URL: `/media/`
     - Directory: `/home/YOUR_USERNAME/sumi-jewelry/media`

8. Run these commands in the PythonAnywhere bash console:
```bash
cd ~/sumi-jewelry
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

9. Reload your web app:
   - Go to "Web" tab
   - Click "Reload" button

10. Your site should now be live at `your-username.pythonanywhere.com`

## Important Notes

- Replace `YOUR_USERNAME` with your PythonAnywhere username
- Keep your `SECRET_KEY` secure and never commit it to version control
- Make sure `DEBUG=False` in production
- Update `ALLOWED_HOSTS` with your actual domain
- For custom domains, configure them in PythonAnywhere's "Web" tab
- Regularly backup your database and media files

## Troubleshooting

- Check PythonAnywhere error logs in the "Web" tab
- Ensure all static files are collected properly
- Verify database migrations are applied
- Check file permissions in your project directory
- Make sure your virtual environment is activated when running commands

## Support

For deployment issues, contact PythonAnywhere support or refer to their documentation at https://help.pythonanywhere.com/ 