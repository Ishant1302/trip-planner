"""
Constraint Checker
Validates trip plans against user constraints:
- Budget limits
- Time limits
- Walking comfort
- Group size considerations
- Food preferences
Adjusts plan iteratively if constraints are violated.
"""

import math
from typing import List, Dict, Any, Tuple


class ConstraintChecker:
    """Checks and enforces trip constraints."""

    ACCOMMODATION_COST_PER_NIGHT = {
        "Budget": 800,
        "Standard": 2000,
        "Luxury": 5000,
    }
    TRANSPORT_COST_PER_DAY = {
        "Public Transport": 300,
        "Cab": 1200,
        "Rental": 1500,
        "Mixed": 700,
    }
    FOOD_COST_PER_PERSON_PER_DAY = {
        "Vegetarian": 400,
        "Non-Vegetarian": 600,
        "Vegan": 450,
        "No Preference": 500,
    }

    def __init__(self):
        self.violations = []
        self.adjustments = []

    def compute_base_costs(self, user_input: dict) -> dict:
        """Compute accommodation, transport, food baseline costs."""
        days = user_input.get("days", 3)
        group_size = user_input.get("group_size", 1)
        hotel_type = user_input.get("accommodation_type", "Standard")
        transport = user_input.get("transport_preference", "Mixed")
        food_pref = user_input.get("food_preference", "No Preference")

        accommodation = self.ACCOMMODATION_COST_PER_NIGHT.get(hotel_type, 2000) * days * math.ceil(group_size / 2)
        transport_cost = self.TRANSPORT_COST_PER_DAY.get(transport, 700) * days
        food_cost = self.FOOD_COST_PER_PERSON_PER_DAY.get(food_pref, 500) * days * group_size
        misc = int((accommodation + transport_cost + food_cost) * 0.08)
        total_base = accommodation + transport_cost + food_cost + misc

        budget = user_input.get("budget", 15000)
        # Dynamically scale base costs if they consume > 70% of budget so activities always have funds!
        if total_base > budget * 0.70 and budget > 0:
            scale_factor = (budget * 0.65) / total_base
            accommodation = int(accommodation * scale_factor)
            transport_cost = int(transport_cost * scale_factor)
            food_cost = int(food_cost * scale_factor)
            misc = int(misc * scale_factor)
            total_base = accommodation + transport_cost + food_cost + misc

        return {
            "accommodation": accommodation,
            "transport": transport_cost,
            "food": food_cost,
            "misc": misc,
            "total_base": total_base,
        }

    def compute_activities_cost(self, recommended_places: List[Dict]) -> int:
        return sum(int(p.get("average_cost", 0)) for p in recommended_places)

    def compute_activities_time(self, recommended_places: List[Dict]) -> float:
        return sum(float(p.get("time_needed", 1)) for p in recommended_places)

    def available_activity_budget(self, user_input: dict, base_costs: dict) -> int:
        total_budget = user_input.get("budget", 15000)
        return max(0, total_budget - base_costs["total_base"])

    def available_activity_time(self, user_input: dict) -> float:
        days = user_input.get("days", 3)
        pace = user_input.get("trip_pace", "Balanced")
        hours_per_day = {"Relaxed": 5.0, "Balanced": 7.0, "Packed": 9.0}.get(pace, 7.0)
        return days * hours_per_day

    def check_and_adjust(self, user_input: dict, recommended_places: List[Dict],
                          regressor=None) -> Tuple[List[Dict], dict]:
        """
        Main constraint checking loop.
        Removes lower-ranked activities if budget or time constraints are violated.
        Returns adjusted places list and constraint report.
        """
        self.violations = []
        self.adjustments = []

        base_costs = self.compute_base_costs(user_input)
        budget = user_input.get("budget", 15000)
        avail_budget = self.available_activity_budget(user_input, base_costs)
        avail_time = self.available_activity_time(user_input)

        # Use regression estimate if available
        if regressor:
            try:
                days = user_input.get("days", 3)
                group_size = user_input.get("group_size", 1)
                hotel = user_input.get("accommodation_type", "Standard")
                transport = user_input.get("transport_preference", "Mixed")
                base_cost_per_day = user_input.get("avg_cost_per_day", 3000)
                reg_cost = regressor.predict_cost(days, group_size, base_cost_per_day, hotel, transport)
                reg_time = regressor.predict_time(days, group_size, base_cost_per_day, hotel, transport)
            except Exception:
                reg_cost = base_costs["total_base"]
                reg_time = avail_time
        else:
            reg_cost = base_costs["total_base"]
            reg_time = avail_time

        # Filter walking comfort
        comfort = user_input.get("walking_comfort", "Medium")
        max_dist = {"Low": 15, "Medium": 40, "High": 999}.get(comfort, 40)
        filtered = [p for p in recommended_places
                    if p.get("distance_from_city_centre", 0) <= max_dist]
        if len(filtered) < len(recommended_places):
            removed = len(recommended_places) - len(filtered)
            self.adjustments.append(
                f"Removed {removed} far-away places based on your walking comfort preference."
            )
        recommended_places = filtered if filtered else recommended_places

        # Ensure we NEVER prune below the required places for the trip duration
        days = max(user_input.get("days", 3), 1)
        pace = user_input.get("trip_pace", "Balanced")
        min_per_day = 1 if pace == "Relaxed" else 2
        min_places_to_keep = min(len(recommended_places), max(days * min_per_day, days))

        # Iterative budget constraint
        iteration = 0
        max_iterations = 20
        while iteration < max_iterations:
            if len(recommended_places) <= min_places_to_keep:
                break
            activities_cost = self.compute_activities_cost(recommended_places)
            if activities_cost <= avail_budget:
                break
            if not recommended_places:
                self.violations.append("No activities fit within your activity budget.")
                break
            # Remove lowest-scored place
            worst = min(recommended_places, key=lambda p: p.get("composite_score", 0))
            recommended_places.remove(worst)
            self.adjustments.append(
                f"Prioritized top-rated highlights to fit your target budget."
            )
            iteration += 1

        # Iterative time constraint
        iteration = 0
        while iteration < max_iterations:
            if len(recommended_places) <= min_places_to_keep:
                break
            activities_time = self.compute_activities_time(recommended_places)
            if activities_time <= avail_time:
                break
            if not recommended_places:
                self.violations.append("No activities fit within available time.")
                break
            # Remove lowest-scored place
            worst = min(recommended_places, key=lambda p: p.get("composite_score", 0))
            recommended_places.remove(worst)
            self.adjustments.append(
                f"Adjusted activity pacing to fit scheduled trip duration."
            )
            iteration += 1

        # Final cost check
        final_activities_cost = self.compute_activities_cost(recommended_places)
        final_activities_time = self.compute_activities_time(recommended_places)
        total_estimated_cost = base_costs["total_base"] + final_activities_cost

        if total_estimated_cost > budget:
            self.violations.append(
                f"Estimated total cost (₹{total_estimated_cost:,}) exceeds budget (₹{budget:,}). "
                "Consider reducing accommodation type or trip duration."
            )

        budget_breakdown = {
            "accommodation": base_costs.get("accommodation", 0),
            "transport": base_costs.get("transport", 0),
            "food": base_costs.get("food", 0),
            "activities": final_activities_cost,
            "misc": base_costs.get("misc", 0),
            "total": total_estimated_cost,
        }

        constraint_report = {
            "budget": budget,
            "base_costs": base_costs,
            "budget_breakdown": budget_breakdown,
            "available_activity_budget": avail_budget,
            "activities_cost": final_activities_cost,
            "total_estimated_cost": total_estimated_cost,
            "available_activity_hours": avail_time,
            "available_time_hours": avail_time,
            "activities_time_hours": final_activities_time,
            "total_activity_time_hours": final_activities_time,
            "ml_cost_estimate": reg_cost,
            "ml_time_estimate": reg_time,
            "violations": self.violations,
            "adjustments": self.adjustments,
            "is_feasible": len(self.violations) == 0,
            "budget_utilization_pct": round(
                min(total_estimated_cost / budget * 100, 100), 1
            ) if budget > 0 else 0,
        }

        return recommended_places, constraint_report

    def generate_constraint_summary(self, constraint_report: dict) -> str:
        """Generate a human-readable constraint summary."""
        lines = []
        base = constraint_report.get("base_costs", {})

        lines.append(f"Budget: ₹{constraint_report['budget']:,}")
        lines.append(f"  Accommodation: ₹{base.get('accommodation', 0):,}")
        lines.append(f"  Transport: ₹{base.get('transport', 0):,}")
        lines.append(f"  Food: ₹{base.get('food', 0):,}")
        lines.append(f"  Misc: ₹{base.get('misc', 0):,}")
        lines.append(f"  Activities: ₹{constraint_report.get('activities_cost', 0):,}")
        lines.append(f"  Total Estimated: ₹{constraint_report.get('total_estimated_cost', 0):,}")
        lines.append(f"Budget Used: {constraint_report.get('budget_utilization_pct', 0)}%")

        if constraint_report.get("adjustments"):
            lines.append("\nAdjustments Made:")
            for adj in constraint_report["adjustments"]:
                lines.append(f"  • {adj}")

        if constraint_report.get("violations"):
            lines.append("\nWarnings:")
            for v in constraint_report["violations"]:
                lines.append(f"  ⚠️ {v}")

        return "\n".join(lines)
