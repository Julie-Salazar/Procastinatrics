from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models.activitylog import ActivityLog
from collections import defaultdict
from calendar import month_name

views = Blueprint('views', __name__)

def get_category_color(category):
    # Assign a color based on the category name
    color_map = {
        "Productive": "#4caf50",
        "Social Media": "#2196f3",
        "Gaming": "#ff9800",
        "Other": "#9e9e9e"
    }
    return color_map.get(category, "#607d8b")  # Default color if category not found

@views.route('/analytics-home', methods=['GET'])
@login_required
def analytics_home():
    """Routing function for analytics-home.

    Returns:
        HTML for analytics-home.
    """
    try:
        # Query the ActivityLog model for the current user's logged activities
        user_logs = ActivityLog.query.filter_by(user_id=current_user.id).order_by(ActivityLog.timestamp.desc()).all()

        # Prepare data for recent logs (limit to the 8 most recent logs)
        recent_logs = [
            {
                "application": log.application or "Unknown",
                "category": log.category or "Other",
                "hours": log.hours or 0,
                "minutes": log.minutes or 0,
                "mood": log.mood or "N/A",
                "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S') if log.timestamp else "N/A"
            }
            for log in user_logs[:8]  # Limit to the 8 most recent logs
        ]

        # Get all unique categories from user logs
        categories = set()
        for log in user_logs:
            categories.add(log.category or "Other")
        
        # Make sure we always include these standard categories even if no logs exist yet
        standard_categories = ["Productive", "Social Media", "Gaming", "Other"]
        for category in standard_categories:
            categories.add(category)
        
        # Create a more complex data structure to track activities by category
        # Initialize data structure with all months and all categories
        productivity_data = {
            "monthly": {
                "labels": list(month_name[1:])  # ['January', 'February', ..., 'December']
            },
            "weekly": {
                "labels": []
            },
            "yearly": {
                "labels": []
            }
        }
        
        # Initialize each category with zeros for all months
        for category in categories:
            category_key = category.lower().replace(' ', '_')  # Convert "Social Media" to "social_media"
            productivity_data["monthly"][category_key] = [0] * 12  # Initialize all months with 0
        
        # Prepare data for productivity chart grouped by year, month, and week
        category_week_totals = defaultdict(lambda: defaultdict(float))  # To track weekly data by category
        category_year_totals = defaultdict(lambda: defaultdict(float))  # To track yearly data by category
        
        weeks = set()  # To track unique weeks
        years = set()  # To track unique years
        
        for log in user_logs:
            if log.timestamp:
                # Convert category to a valid key
                category = log.category or "Other"
                category_key = category.lower().replace(' ', '_')
                
                # Calculate hours including minutes
                hours = (log.hours or 0) + ((log.minutes or 0) / 60)
                
                # Group by month
                month_index = log.timestamp.month - 1  # 0-based index for months
                productivity_data["monthly"][category_key][month_index] += hours
                
                # Track weeks
                week = log.timestamp.strftime('%U')  # Week number of the year (00-53)
                weeks.add(week)
                category_week_totals[week][category_key] += hours
                
                # Track years
                year = log.timestamp.strftime('%Y')
                years.add(year)
                category_year_totals[year][category_key] += hours
        
        # Sort weeks and years
        sorted_weeks = sorted(weeks)
        sorted_years = sorted(years)
        
        # Update the productivity_data structure with weekly data
        productivity_data["weekly"]["labels"] = sorted_weeks
        for category in categories:
            category_key = category.lower().replace(' ', '_')
            productivity_data["weekly"][category_key] = []
            for week in sorted_weeks:
                productivity_data["weekly"][category_key].append(category_week_totals[week][category_key])
        
        # Update the productivity_data structure with yearly data
        productivity_data["yearly"]["labels"] = sorted_years
        for category in categories:
            category_key = category.lower().replace(' ', '_')
            productivity_data["yearly"][category_key] = []
            for year in sorted_years:
                productivity_data["yearly"][category_key].append(category_year_totals[year][category_key])
        
        # Prepare data for procrastination breakdown
        procrastination_breakdown = {"totalHours": 0, "categories": []}
        category_totals = defaultdict(int)
        for log in user_logs:
            total_hours = (log.hours or 0) * 60 + (log.minutes or 0)
            category_totals[log.category or "Other"] += total_hours

        # Convert category totals into percentages
        total_hours_logged = sum(category_totals.values())
        for category, minutes in category_totals.items():
            percentage = (minutes / total_hours_logged) * 100 if total_hours_logged > 0 else 0
            procrastination_breakdown["categories"].append({
                "name": category,
                "percentage": round(percentage, 2),
                "color": get_category_color(category)  # Helper function to assign colors
            })
        procrastination_breakdown["totalHours"] = total_hours_logged // 60

        # Debugging: Print data structures
        print("Productivity Data (Monthly):", productivity_data["monthly"])
        print("Productivity Data (Weekly):", productivity_data["weekly"])
        print("Productivity Data (Yearly):", productivity_data["yearly"])
        print("Procrastination Breakdown:", procrastination_breakdown)

        # Combine all data into a single dictionary
        logs_data = {
            "recentLogs": recent_logs,
            "productivityData": productivity_data,
            "procrastinationBreakdown": procrastination_breakdown
        }

        # Pass the data to the template
        return render_template('analytics-home.html', logs_data=logs_data)

    except Exception as e:
        # Print the error to the console for debugging
        print("Error:", e)
        return "An error occurred while processing the request.", 500