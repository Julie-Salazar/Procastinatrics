from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models.activitylog import ActivityLog
from collections import defaultdict

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
    try:
        # Query the ActivityLog model for the current user's logged activities
        user_logs = ActivityLog.query.filter_by(user_id=current_user.id).order_by(ActivityLog.timestamp.desc()).all()

        # Prepare data for recent logs
        recent_logs = [
            {
                "application": log.application or "Unknown",
                "category": log.category or "Other",
                "time_spent_hours": log.hours or 0, 
                "mood": log.mood or "N/A",
                "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S') if log.timestamp else "N/A"
            }
            for log in user_logs[:5]  # Limit to the 5 most recent logs
        ]

        # Debugging: Print recent logs
        print("Recent Logs:", recent_logs)

        # Prepare data for productivity chart grouped by year, month, and week
        productivity_data = defaultdict(lambda: {"labels": [], "productivity": []})
        for log in user_logs:
            if log.timestamp:
                # Group by year
                year = log.timestamp.strftime('%Y')
                if year not in productivity_data["yearly"]["labels"]:
                    productivity_data["yearly"]["labels"].append(year)
                    productivity_data["yearly"]["productivity"].append(log.hours or 0)
                else:
                    index = productivity_data["yearly"]["labels"].index(year)
                    productivity_data["yearly"]["productivity"][index] += log.hours or 0

                # Group by month
                month = log.timestamp.strftime('%B')
                if month not in productivity_data["monthly"]["labels"]:
                    productivity_data["monthly"]["labels"].append(month)
                    productivity_data["monthly"]["productivity"].append(log.hours or 0)
                else:
                    index = productivity_data["monthly"]["labels"].index(month)
                    productivity_data["monthly"]["productivity"][index] += log.hours or 0

                # Group by week
                week = log.timestamp.strftime('%U')  # Week number of the year (00-53)
                if week not in productivity_data["weekly"]["labels"]:
                    productivity_data["weekly"]["labels"].append(week)
                    productivity_data["weekly"]["productivity"].append(log.hours or 0)
                else:
                    index = productivity_data["weekly"]["labels"].index(week)
                    productivity_data["weekly"]["productivity"][index] += log.hours or 0

        # Debugging: Print productivity data
        print("Productivity Data (Yearly):", productivity_data["yearly"])
        print("Productivity Data (Monthly):", productivity_data["monthly"])
        print("Productivity Data (Weekly):", productivity_data["weekly"])

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

        # Debugging: Print procrastination breakdown
        print("Procrastination Breakdown:", procrastination_breakdown)

        # Combine all data into a single dictionary
        logs_data = {
            "recentLogs": recent_logs,
            "productivityData": dict(productivity_data),
            "procrastinationBreakdown": procrastination_breakdown
        }

        # Debugging: Print logs_data
        print("Logs Data:", logs_data)

        # Pass the data to the template
        return render_template('analytics-home.html', logs_data=logs_data)

    except Exception as e:
        # Print the error to the console for debugging
        print("Error:", e)
        return "An error occurred while processing the request.", 500