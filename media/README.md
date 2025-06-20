# Product Images Directory

This directory contains all product images for the Sumi Jewelry Store.

## Directory Structure
```
media/
└── products/          # Product images
    ├── necklaces/     # Necklace images
    ├── rings/         # Ring images
    ├── earrings/      # Earring images
    └── bracelets/     # Bracelet images
```

## Image Requirements

### General Guidelines
1. **File Formats**: Use .jpg or .png format
2. **Image Size**: 
   - Recommended size: 800x800 pixels
   - Minimum size: 400x400 pixels
   - Maximum file size: 2MB
3. **Image Quality**:
   - High resolution
   - Well-lit
   - Clear background
   - Product should be centered
   - Multiple angles for each product (if possible)

### Naming Convention
- Use lowercase letters
- Use hyphens (-) instead of spaces
- Include product type and name
- Example: `diamond-necklace-1.jpg`, `gold-ring-2.jpg`

### Image Optimization
Before uploading:
1. Compress images to reduce file size
2. Ensure proper lighting and color balance
3. Remove any watermarks or unnecessary elements
4. Use a consistent background color

## How to Add Images

1. Through Django Admin:
   - Log in to the admin interface
   - Navigate to Products
   - Select a product
   - Click on the image field
   - Upload the image
   - Save the product

2. Through File System:
   - Place images in appropriate subdirectories
   - Follow the naming convention
   - Ensure proper permissions

## Best Practices
1. Always maintain a backup of original images
2. Keep image sizes consistent across similar products
3. Use descriptive filenames
4. Regularly clean up unused images
5. Optimize images for web use

## Image Processing
The system will automatically:
- Create thumbnails for product listings
- Maintain aspect ratios
- Optimize images for web delivery 