import streamlit as st
from datetime import datetime

from api import (
    create_trip,
    get_trips,
    get_trip,
    delete_trip
)

from styles import load_css


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="BudgetYatta",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()


# =========================================================
# SESSION STATE
# =========================================================

if "selected_trip" not in st.session_state:
    st.session_state.selected_trip = None


# =========================================================
# HEADER
# =========================================================

st.title("✈️ BudgetYatta")

st.caption(
    "Plan smarter. Travel better. "
    "Create AI-powered trips within your budget."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🧭 BudgetYatta")

    page = st.radio(
        "Navigation",
        [
            "🌍 Plan My Trip",
            "📚 My Previous Trips"
        ]
    )

    st.divider()

    st.markdown(
        """
        ### ✈️ About BudgetYatta

        BudgetYatta is an AI-powered travel
        planner that creates personalized
        itineraries according to your:

        - Destination
        - Duration
        - Travellers
        - Budget
        - Accommodation
        - Interests
        """
    )

    st.divider()

    st.caption(
        "AI Travel Planner • Full Stack Project"
    )


# =========================================================
# PLAN MY TRIP
# =========================================================

if page == "🌍 Plan My Trip":

    st.header("🌍 Create Your Travel Plan")

    st.write(
        "Enter your travel requirements and "
        "let BudgetYatta create a personalized itinerary."
    )

    st.write("")

    # -----------------------------------------------------
    # FORM
    # -----------------------------------------------------

    with st.form("travel_form"):

        st.subheader("📝 Trip Details")

        col1, col2 = st.columns(2)

        with col1:

            destination = st.text_input(
                "📍 Destination",
                placeholder="Example: Jaipur"
            )

            duration = st.number_input(
                "📅 Number of Days",
                min_value=1,
                max_value=30,
                value=3,
                step=1
            )

            travellers = st.number_input(
                "👥 Number of Travellers",
                min_value=1,
                max_value=50,
                value=2,
                step=1
            )

        with col2:

            budget = st.number_input(
                "💰 Total Budget (₹)",
                min_value=1000.0,
                value=15000.0,
                step=1000.0
            )

            accommodation = st.selectbox(
                "🏨 Accommodation Preference",
                [
                    "Budget",
                    "Standard",
                    "Premium",
                    "Luxury"
                ]
            )

            interests = st.text_input(
                "❤️ Travel Interests",
                placeholder="Food, Culture, Shopping"
            )

        st.write("")

        submitted = st.form_submit_button(
            "✨ Generate My Trip",
            use_container_width=True,
            type="primary"
        )

    # -----------------------------------------------------
    # GENERATE TRIP
    # -----------------------------------------------------

    if submitted:

        if not destination.strip():

            st.error(
                "❌ Please enter your destination."
            )

        elif not interests.strip():

            st.error(
                "❌ Please enter at least one travel interest."
            )

        elif budget <= 0:

            st.error(
                "❌ Budget must be greater than zero."
            )

        else:

            request_data = {
                "destination": destination.strip(),
                "duration": int(duration),
                "travellers": int(travellers),
                "budget": float(budget),
                "accommodation": accommodation,
                "interests": interests.strip()
            }

            with st.spinner(
                "🤖 BudgetYatta AI is creating your trip..."
            ):

                try:

                    trip = create_trip(
                        request_data
                    )

                    st.session_state.selected_trip = trip

                    st.success(
                        "🎉 Your trip has been created successfully!"
                    )

                except Exception as error:

                    st.error(
                        f"❌ Unable to create trip: {error}"
                    )


# =========================================================
# DISPLAY GENERATED TRIP
# =========================================================

if (
    page == "🌍 Plan My Trip"
    and st.session_state.selected_trip
):

    trip = st.session_state.selected_trip

    itinerary = trip["itinerary"]

    st.divider()

    st.header(
        f"🗺️ Your {trip['destination']} Trip"
    )

    # -----------------------------------------------------
    # TRIP SUMMARY METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📍 Destination",
            trip["destination"]
        )

    with col2:

        st.metric(
            "📅 Duration",
            f"{trip['duration']} Days"
        )

    with col3:

        st.metric(
            "👥 Travellers",
            str(trip["travellers"])
        )

    with col4:

        st.metric(
            "💰 Budget",
            f"₹{trip['budget']:,.0f}"
        )

    st.write("")

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    st.subheader("✨ Trip Summary")

    st.info(
        itinerary.get(
            "summary",
            "Your personalized travel plan is ready."
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**🏨 Accommodation:** "
            f"{trip['accommodation']}"
        )

    with col2:

        st.write(
            f"**❤️ Interests:** "
            f"{trip['interests']}"
        )

    # -----------------------------------------------------
    # DAY BY DAY ITINERARY
    # -----------------------------------------------------

    st.divider()

    st.header("📅 Day-by-Day Itinerary")

    days = itinerary.get(
        "days",
        []
    )

    if not days:

        st.warning(
            "No daily itinerary was generated."
        )

    else:

        for day in days:

            day_number = day.get(
                "day",
                ""
            )

            title = day.get(
                "title",
                f"Day {day_number}"
            )

            with st.expander(
                f"Day {day_number} — {title}",
                expanded=True
            ):

                # Places

                st.markdown(
                    "### 📍 Places to Visit"
                )

                places = day.get(
                    "places",
                    []
                )

                if places:

                    for place in places:

                        st.write(
                            f"• {place}"
                        )

                else:

                    st.write(
                        "No places provided."
                    )

                # Activities

                st.markdown(
                    "### 🎯 Activities"
                )

                activities = day.get(
                    "activities",
                    []
                )

                if activities:

                    for activity in activities:

                        st.write(
                            f"• {activity}"
                        )

                else:

                    st.write(
                        "No activities provided."
                    )

                # Food

                st.markdown(
                    "### 🍴 Food & Experiences"
                )

                food = day.get(
                    "food",
                    []
                )

                if food:

                    for item in food:

                        st.write(
                            f"• {item}"
                        )

                else:

                    st.write(
                        "No food recommendations provided."
                    )

                # Daily cost

                daily_cost = day.get(
                    "approximate_cost",
                    0
                )

                st.write("")

                st.metric(
                    "💰 Approximate Day Cost",
                    f"₹{float(daily_cost):,.0f}"
                )


    # =====================================================
    # EXPENSE BREAKDOWN
    # =====================================================

    st.divider()

    st.header("💰 Estimated Expenses")

    expenses = itinerary.get(
        "expenses",
        []
    )

    if expenses:

        expense_columns = st.columns(
            min(len(expenses), 5)
        )

        for index, expense in enumerate(expenses):

            column = expense_columns[
                index % len(expense_columns)
            ]

            with column:

                category = expense.get(
                    "category",
                    "Other"
                )

                amount = expense.get(
                    "estimated_cost",
                    0
                )

                st.metric(
                    category,
                    f"₹{float(amount):,.0f}"
                )

    else:

        st.info(
            "Expense breakdown is not available."
        )

    # -----------------------------------------------------
    # TOTAL COST
    # -----------------------------------------------------

    total_cost = itinerary.get(
        "total_estimated_cost",
        trip.get(
            "estimated_cost",
            0
        )
    )

    st.write("")

    st.success(
        f"💵 Total Estimated Cost: "
        f"₹{float(total_cost):,.0f}"
    )

    # -----------------------------------------------------
    # BUDGET COMPARISON
    # -----------------------------------------------------

    user_budget = float(
        trip["budget"]
    )

    estimated_cost = float(
        total_cost
    )

    difference = user_budget - estimated_cost

    if difference > 0:

        st.info(
            f"💚 Estimated savings within budget: "
            f"₹{difference:,.0f}"
        )

    elif difference == 0:

        st.info(
            "🎯 The estimated trip cost matches your budget."
        )

    else:

        st.warning(
            f"⚠️ Estimated cost is "
            f"₹{abs(difference):,.0f} above your budget."
        )


# =========================================================
# PREVIOUS TRIPS
# =========================================================

if page == "📚 My Previous Trips":

    st.header("📚 My Previous Trips")

    st.write(
        "View and manage your previously generated trips."
    )

    st.divider()

    try:

        trips = get_trips()

        if not trips:

            st.info(
                "🧳 No previous trips found."
            )

            st.write(
                "Create your first trip from "
                "'Plan My Trip'."
            )

        else:

            st.subheader(
                f"🗂️ Saved Trips ({len(trips)})"
            )

            for trip in trips:

                created = trip.get(
                    "created_at",
                    ""
                )

                try:

                    created_date = (
                        datetime.fromisoformat(
                            created.replace(
                                "Z",
                                ""
                            )
                        ).strftime(
                            "%d %B %Y"
                        )
                    )

                except Exception:

                    created_date = str(
                        created
                    )

                col1, col2, col3 = st.columns(
                    [5, 1.5, 1]
                )

                with col1:

                    st.markdown(
                        f"### 📍 {trip['destination']}"
                    )

                    st.write(
                        f"📅 {trip['duration']} Days "
                        f"• 👥 {trip['travellers']} Travellers "
                        f"• 💰 ₹{trip['budget']:,.0f}"
                    )

                    st.caption(
                        f"Created: {created_date}"
                    )

                with col2:

                    if st.button(
                        "👁️ View",
                        key=f"view_{trip['id']}",
                        use_container_width=True
                    ):

                        try:

                            selected = get_trip(
                                trip["id"]
                            )

                            st.session_state.selected_trip = (
                                selected
                            )

                            st.rerun()

                        except Exception as error:

                            st.error(
                                f"Unable to open trip: {error}"
                            )

                with col3:

                    if st.button(
                        "🗑️",
                        key=f"delete_{trip['id']}",
                        use_container_width=True
                    ):

                        try:

                            delete_trip(
                                trip["id"]
                            )

                            if (
                                st.session_state.selected_trip
                                and st.session_state.selected_trip.get(
                                    "id"
                                ) == trip["id"]
                            ):

                                st.session_state.selected_trip = None

                            st.success(
                                "Trip deleted successfully."
                            )

                            st.rerun()

                        except Exception as error:

                            st.error(
                                f"Unable to delete trip: {error}"
                            )

                st.divider()


    except Exception as error:

        st.error(
            f"❌ Could not load previous trips: {error}"
        )


# =========================================================
# PREVIOUS TRIP DETAILS
# =========================================================

if (
    page == "📚 My Previous Trips"
    and st.session_state.selected_trip
):

    trip = st.session_state.selected_trip

    st.divider()

    st.header(
        f"🗺️ {trip['destination']} Trip Details"
    )

    # -----------------------------------------------------
    # DETAILS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📍 Destination",
            trip["destination"]
        )

    with col2:

        st.metric(
            "📅 Duration",
            f"{trip['duration']} Days"
        )

    with col3:

        st.metric(
            "👥 Travellers",
            str(trip["travellers"])
        )

    with col4:

        st.metric(
            "💰 Budget",
            f"₹{trip['budget']:,.0f}"
        )

    itinerary = trip["itinerary"]

    st.write("")

    st.subheader("✨ Trip Summary")

    st.info(
        itinerary.get(
            "summary",
            "Saved travel itinerary."
        )
    )

    st.write(
        f"**🏨 Accommodation:** "
        f"{trip['accommodation']}"
    )

    st.write(
        f"**❤️ Interests:** "
        f"{trip['interests']}"
    )

    # -----------------------------------------------------
    # DAYS
    # -----------------------------------------------------

    st.divider()

    st.header("📅 Itinerary")

    for day in itinerary.get(
        "days",
        []
    ):

        with st.expander(
            f"Day {day.get('day')} — "
            f"{day.get('title', '')}",
            expanded=True
        ):

            st.markdown(
                "### 📍 Places"
            )

            for place in day.get(
                "places",
                []
            ):

                st.write(
                    f"• {place}"
                )

            st.markdown(
                "### 🎯 Activities"
            )

            for activity in day.get(
                "activities",
                []
            ):

                st.write(
                    f"• {activity}"
                )

            st.markdown(
                "### 🍴 Food"
            )

            for food in day.get(
                "food",
                []
            ):

                st.write(
                    f"• {food}"
                )

            st.write(
                f"💰 Approximate Cost: "
                f"₹{float(day.get('approximate_cost', 0)):,.0f}"
            )

    # -----------------------------------------------------
    # EXPENSES
    # -----------------------------------------------------

    st.divider()

    st.header("💰 Expense Breakdown")

    for expense in itinerary.get(
        "expenses",
        []
    ):

        category = expense.get(
            "category",
            "Other"
        )

        amount = expense.get(
            "estimated_cost",
            0
        )

        st.write(
            f"**{category}** — "
            f"₹{float(amount):,.0f}"
        )

    total_cost = itinerary.get(
        "total_estimated_cost",
        trip.get(
            "estimated_cost",
            0
        )
    )

    st.success(
        f"💵 Total Estimated Cost: "
        f"₹{float(total_cost):,.0f}"
    )
