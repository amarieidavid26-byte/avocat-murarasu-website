#!/usr/bin/env python3
import os
import re

# Image dimensions mapping
IMAGE_DIMENSIONS = {
    'andreea-01.jpeg': (876, 1188),
    'law-library-01.jpeg': (505, 284),
    'columns-01.jpeg': (1000, 667)
}

# Hero image mapping
HERO_IMAGES = {
    'pages/homepage.html': '/public/images/andreea-01.jpeg',
    'pages/about.html': '/public/images/law-library-01.jpeg',
    'pages/practice_areas.html': '/public/images/columns-01.jpeg'
}

def update_image_attributes(content, filepath):
    """Update image attributes for performance"""
    updated_count = 0
    
    # Find all local images
    local_img_pattern = r'<img([^>]*?)src="/public/images/([^"]*?)"([^>]*?)>'
    
    def replace_img(match):
        nonlocal updated_count
        before_src = match.group(1)
        img_name = match.group(2)
        after_src = match.group(3)
        
        # Get dimensions
        width, height = IMAGE_DIMENSIONS.get(img_name, (0, 0))
        
        # Determine if this is a hero image
        is_hero = False
        for hero_file, hero_src in HERO_IMAGES.items():
            if filepath == hero_file and f'/public/images/{img_name}' == hero_src:
                is_hero = True
                break
        
        # Build attributes
        attrs = []
        
        # Add existing attributes (excluding ones we'll replace)
        existing_attrs = before_src + after_src
        existing_attrs = re.sub(r'\s+(loading|decoding|fetchpriority|width|height|onerror)=["\'][^"\']*["\']', '', existing_attrs)
        
        # Add performance attributes
        if is_hero:
            attrs.extend([
                'loading="eager"',
                'fetchpriority="high"',
                'decoding="async"'
            ])
        else:
            attrs.extend([
                'loading="lazy"',
                'decoding="async"'
            ])
        
        # Add dimensions
        if width > 0 and height > 0:
            attrs.extend([
                f'width="{width}"',
                f'height="{height}"'
            ])
        
        # Combine all attributes
        all_attrs = existing_attrs + ' ' + ' '.join(attrs)
        
        updated_count += 1
        return f'<img{all_attrs}src="/public/images/{img_name}">'
    
    updated_content = re.sub(local_img_pattern, replace_img, content)
    return updated_content, updated_count

def add_hero_preload(content, filepath):
    """Add hero image preload link"""
    if filepath not in HERO_IMAGES:
        return content, False
    
    hero_src = HERO_IMAGES[filepath]
    
    # Check if preload already exists
    if f'rel="preload" as="image" href="{hero_src}"' in content:
        return content, True  # Already exists
    
    # Create preload link
    preload_link = f'    <link rel="preload" as="image" href="{hero_src}">'
    
    # Find insertion point (after meta tags, before stylesheets)
    insertion_point = '</head>'
    if '<link rel="stylesheet"' in content:
        insertion_point = '<link rel="stylesheet"'
    
    # Insert preload link
    updated_content = content.replace(insertion_point, f'{preload_link}\n{insertion_point}')
    return updated_content, False

def process_file(filepath):
    """Process a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update image attributes
        updated_content, img_count = update_image_attributes(content, filepath)
        
        # Add hero preload
        final_content, preload_exists = add_hero_preload(updated_content, filepath)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        return img_count, preload_exists
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0, False

# Process all HTML files
html_files = []
for root, dirs, files in os.walk('pages'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

print("Processing HTML files for image optimization...")
total_updated = 0
preload_status = {}

for filepath in html_files:
    img_count, preload_exists = process_file(filepath)
    total_updated += img_count
    preload_status[filepath] = "ALREADY" if preload_exists else ("YES" if img_count > 0 and filepath in HERO_IMAGES else "N/A")
    
    if img_count > 0 or filepath in HERO_IMAGES:
        print(f"✓ {filepath}: {img_count} images updated, preload: {preload_status[filepath]}")

print(f"\nTotal images updated: {total_updated}")

# Show preload status for hero pages
print("\nHero preload status:")
for hero_file in HERO_IMAGES:
    print(f"  {hero_file}: {preload_status[hero_file]}")
