# Updated receipt_helper.py - with calculate_percentages moved here
from app.models.activitylog import ActivityLog
from app.models.receipts import Receipts
from app import db
from collections import defaultdict

def calculate_percentages(user_id):
    """Calculate the actual percentages for a user from their activity logs"""
    # Query user logs
    user_logs = ActivityLog.query.filter_by(user_id=user_id).all()
    
    # Debug each activity log to see categories
    print(f"DEBUG - Activity logs for user {user_id}:")
    categories_found = set()
    for log in user_logs:
        categories_found.add(log.category)
        print(f"  Category: {log.category}, Hours: {log.hours or 0}, Minutes: {log.minutes or 0}")
    
    print(f"DEBUG - Unique categories found: {', '.join(categories_found)}")
    
    # Calculate total hours logged
    total_hours = sum((log.hours or 0) + (log.minutes or 0) / 60 for log in user_logs)
    
    # Define category mappings (case-insensitive)
    category_mapping = {
        'productive': 'Productive',
        'productivity': 'Productive',
        'work': 'Productive',
        'study': 'Productive',
        'learning': 'Productive',
        
        'gaming': 'Gaming',
        'games': 'Gaming',
        'game': 'Gaming',
        'videogames': 'Gaming',
        'video games': 'Gaming',
        
        'social media': 'Social Media',
        'social': 'Social Media',
        'media': 'Social Media',
        
        # Add more mappings as needed
    }
    
    # Calculate category percentages with normalized categories
    category_totals = defaultdict(float)
    for log in user_logs:
        hours = (log.hours or 0) + (log.minutes or 0) / 60
        
        # Normalize category (case-insensitive)
        category_lower = log.category.lower() if log.category else "other"
        normalized_category = category_mapping.get(category_lower, "Other")
        
        category_totals[normalized_category] += hours
    
    # Debug normalized category totals
    print(f"DEBUG - Normalized category totals:")
    for category, hours in category_totals.items():
        percentage = (hours / total_hours) * 100 if total_hours > 0 else 0
        print(f"  {category}: {hours} hours ({round(percentage)}%)")
    
    # Calculate percentages
    category_percentages = {}
    for category, hours in category_totals.items():
        percentage = (hours / total_hours) * 100 if total_hours > 0 else 0
        category_percentages[category] = round(percentage)
    
    # Get productive, gaming, and procrastination percentages
    productive_percent = category_percentages.get("Productive", 0)
    gaming_percent = category_percentages.get("Gaming", 0)
    social_percent = category_percentages.get("Social Media", 0)
    other_percent = category_percentages.get("Other", 0)
    
    # Combined procrastination percent (social + other)
    procrastination_percent = social_percent + other_percent
    
    # Ensure percentages add up to 100%
    total_percent = productive_percent + gaming_percent + procrastination_percent
    if total_percent != 100 and total_hours > 0:
        # Adjust the largest category to make total 100%
        adjustment = 100 - total_percent
        if productive_percent >= gaming_percent and productive_percent >= procrastination_percent:
            productive_percent += adjustment
        elif gaming_percent >= productive_percent and gaming_percent >= procrastination_percent:
            gaming_percent += adjustment
        else:
            procrastination_percent += adjustment
    
    # Debug final percentages
    print(f"DEBUG - Final percentages:")
    print(f"  Productive: {productive_percent}%")
    print(f"  Gaming: {gaming_percent}%")
    print(f"  Procrastination: {procrastination_percent}%")
    print(f"  Total Hours: {round(total_hours)}")
    
    return {
        "procrastination_percent": procrastination_percent,
        "gaming_percent": gaming_percent,
        "productive_percent": productive_percent,
        "total_hours": round(total_hours)
    }

def ensure_receipt_percentages(receipt):
    """
    Ensures the receipt has calculated percentage values.
    If all tracked hours are 0, it populates them based on activity logs.
    
    Args:
        receipt (Receipts): The receipt SQLAlchemy object to update.
    """
    if receipt and (
        receipt.hours_procrastinated == 0 and 
        receipt.hours_gaming == 0 and 
        receipt.hours_productive == 0
    ):
        percentages = calculate_percentages(receipt.author_id)
        receipt.hours_procrastinated = percentages["procrastination_percent"]
        receipt.hours_gaming = percentages["gaming_percent"]
        receipt.hours_productive = percentages["productive_percent"]
        db.session.commit()
        return percentages
    return None