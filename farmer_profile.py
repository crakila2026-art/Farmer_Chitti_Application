
import streamlit as st

def render_farmer_profile():

    st.subheader("Farmer Registration")

    with st.form("farmer_profile_form"):

        name = st.text_input("Farmer Name")

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30
        )

        mobile = st.text_input("Mobile Number")

        state = st.selectbox(
            "State",
            ["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh"]
        )

        district = st.text_input("District")

        village = st.text_input("Village")

        land_ownership = st.selectbox(
            "Land Ownership",
            ["Own Land", "Leased Land", "Tenant Farmer", "Landless"]
        )

        land_acres = st.number_input(
            "Land Size (Acres)",
            min_value=0.0,
            max_value=1000.0,
            value=1.0,
            step=0.25
        )

        crop = st.selectbox(
            "Primary Crop",
            [
                "Paddy",
                "Sugarcane",
                "Groundnut",
                "Cotton",
                "Banana",
                "Vegetables",
                "Other"
            ]
        )

        irrigation = st.selectbox(
            "Irrigation Type",
            ["Rainfed", "Borewell", "Canal", "Drip", "Other"]
        )

        annual_income = st.number_input(
            "Annual Household Income (₹)",
            min_value=0,
            value=100000,
            step=10000
        )

        submitted = st.form_submit_button(
            "Save Farmer Profile"
        )

        if submitted:

            if not name.strip() or not district.strip():
                st.error("Please enter farmer name and district.")

            elif len(mobile.strip()) != 10 or not mobile.strip().isdigit():
                st.error("Enter a valid 10-digit mobile number.")

            else:

                profile = {
                    "name": name.strip(),
                    "age": age,
                    "mobile": mobile.strip(),
                    "state": state,
                    "district": district.strip(),
                    "village": village.strip(),
                    "land_ownership": land_ownership,
                    "land_acres": land_acres,
                    "crop": crop,
                    "irrigation": irrigation,
                    "annual_income": annual_income
                }

                st.session_state["farmer_profile"] = profile

                st.success("Farmer profile saved successfully!")

                st.json(profile)

                return profile

    return st.session_state.get("farmer_profile")
