
def assess_scheme(profile, scheme):

    missing_information = []
    reasons = []

    if not profile.get("state"):
        missing_information.append("State")

    if not profile.get("district"):
        missing_information.append("District")

    if not profile.get("crop"):
        missing_information.append("Crop")

    if not profile.get("land_ownership"):
        missing_information.append("Land ownership")

    if missing_information:
        return {
            "scheme": scheme,
            "status": "Needs More Information",
            "reasons": missing_information
        }

    # Preliminary matching only.
    # Actual criteria must come from verified
    # official scheme guidelines.

    if scheme == "PM-KISAN":

        if profile["land_ownership"] != "Own Land":
            return {
                "scheme": scheme,
                "status": "Potentially Not Eligible",
                "reasons": [
                    "Land ownership requires verification"
                ]
            }

        return {
            "scheme": scheme,
            "status": "Potentially Eligible",
            "reasons": [
                "Land ownership condition needs verification",
                "Applicable exclusion criteria must be checked"
            ]
        }

    return {
        "scheme": scheme,
        "status": "Needs Scheme-Specific Assessment",
        "reasons": [
            "Scheme-specific official criteria need to be evaluated"
        ]
    }
