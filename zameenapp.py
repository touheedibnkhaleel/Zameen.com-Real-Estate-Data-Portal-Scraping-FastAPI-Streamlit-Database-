import streamlit as st
import requests

st.title("Real Estate Data Portal")

base_url = 'http://127.0.0.1:8000'

option = st.radio("Choose an action:", ["Search Properties", "Get Property by ID", "Get All Properties"])

if option == "Search Properties":
    location = st.text_input("Location (e.g., Islamabad)")
    property_type = st.selectbox("property_type", ["", "house", "plot", "flat"])
    min_price = st.number_input("Min Price", min_value=0, step=100000)
    max_price = st.number_input("Max Price", min_value=0, step=100000)

    if st.button("Search"):
        params = {}
        if location:
            params["location"] = location
        if property_type:
            params["property_type"] = property_type
        if min_price > 0:
            params["min_price"] = min_price
        if max_price > 0:
            params["max_price"] = max_price

        try:
            resp = requests.get(f"{base_url}/properties/search", params=params, timeout=15)
            resp.raise_for_status()
            result = resp.json()
            properties = result.get("data") if isinstance(result, dict) else result
            properties = properties or []
            st.subheader(f"Found {len(properties)} Properties")
            if properties:
                st.dataframe(properties)
            else:
                st.warning("No properties found for the given filters.")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch properties from FastAPI: {e}")

elif option == "Get Property by ID":
    property_id = st.number_input("Enter Property ID", min_value=1, step=1)
    if st.button("Get Property"):
        try:
            resp = requests.get(f"{base_url}/properties/{property_id}", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and data.get("error"):
                st.warning(data["error"])
            else:
                st.json(data)
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch property from FastAPI: {e}")

elif option == "Get All Properties":
    max_display = st.number_input("Max rows to display (0 = show all)", min_value=0, value=100, step=50)
    if st.button("Fetch All Properties"):
        try:
            resp = requests.get(f"{base_url}/properties", timeout=30)
            resp.raise_for_status()
            data = resp.json()
            properties = data.get("data") if isinstance(data, dict) and data.get("data") else (data if isinstance(data, list) else [])
            total = len(properties)
            if total == 0:
                st.warning("No properties returned by the API.")
            else:
                st.subheader(f"Total properties returned: {total}")
                if max_display > 0 and total > max_display:
                    st.info(f"Showing first {max_display} rows (use 0 to show all).")
                    st.dataframe(properties[:max_display])
                else:
                    st.dataframe(properties)
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch properties from FastAPI: {e}")