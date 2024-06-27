import streamlit as st
import pandas as pd
import hmac

st.title("View data")

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["code"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

st.write("The goal of this prototype is to allow you to interact with Fin as if it were integrated with your financial data. This prototype has data pre-ingested to achieve that goal.")
st.write("The data ingested is a mix of two fictional sources: a Robinhood account with some small positions in stocks and a balance sheet of a high net worth individual. This mix mimics a real life portfolio that has many accounts.")

st.write("### Preview the data below:")

holdings_hard = {
  "F": {
    "price": "11.849900",
    "quantity": "4.00000000",
    "average_buy_price": "12.5000",
    "equity": "47.40",
    "percent_change": "-5.20",
    "intraday_percent_change": "0.00",
    "equity_change": "-2.600400",
    "type": "stock",
    "name": "Ford Motor",
    "id": "6df56bd0-0bf2-44ab-8875-f94fd8526942",
    "pe_ratio": "12.206200",
    "percentage": "36.83"
  },
  "TSLA": {
    "price": "182.850000",
    "quantity": "0.25930500",
    "average_buy_price": "192.8231",
    "equity": "47.41",
    "percent_change": "-5.17",
    "intraday_percent_change": "0.00",
    "equity_change": "-2.586075",
    "type": "stock",
    "name": "Tesla",
    "id": "e39ed23a-7bd1-4587-b060-71988d9ef483",
    "pe_ratio": "46.767400",
    "percentage": "36.84"
  },
  "ARWR": {
    "price": "25.500000",
    "quantity": "0.29200400",
    "average_buy_price": "85.6153",
    "equity": "7.45",
    "percent_change": "-70.22",
    "intraday_percent_change": "0.00",
    "equity_change": "-17.553908",
    "type": "stock",
    "name": "Arrowhead Pharmaceuticals",
    "id": "03ca097b-aed1-47cc-8c8a-073e11491933",
    "pe_ratio": "-6.020000",
    "percentage": "5.78"
  },
  "QCLN": {
    "price": "34.550000",
    "quantity": "0.74872600",
    "average_buy_price": "66.7400",
    "equity": "25.87",
    "percent_change": "-48.23",
    "intraday_percent_change": "0.00",
    "equity_change": "-24.101490",
    "type": "etp",
    "name": "First Trust NASDAQ Clean Edge Green Energy Index Fund",
    "id": "bc0e47d9-eb09-4097-88af-10fd22e78fab",
    "pe_ratio": "0",
    "percentage": "20.10"
  },
  "SPCE": {
    "price": "9.560000",
    "quantity": "0.06137200",
    "average_buy_price": "407.3520",
    "equity": "0.59",
    "percent_change": "-97.65",
    "intraday_percent_change": "0.00",
    "equity_change": "-24.413291",
    "type": "stock",
    "name": "Virgin Galactic Holdings",
    "id": "7b166dc2-333f-4626-9dd9-2759741bac02",
    "pe_ratio": "-0.380000",
    "percentage": "0.46"
  }
}

user_profile_hard = {
  "equity": "138.3762",
  "extended_hours_equity": "138.3848",
  "cash": "9.67",
  "dividend_total": 9.67
}


st.write("#### Robin Hood")
profile = []
col1, col2 = st.columns(2)

with col1:
   st.metric(label='Equity', value=f"${float(user_profile_hard['equity']):,.2f}")

with col2:
   st.metric(label='Cash', value=f"${float(user_profile_hard['cash']):,.2f}")

stocks = []
st.write("##### Stocks")
for symbol, details in holdings_hard.items():
    arrow = "↑" if float(details['percent_change']) > 0 else "↓"
    stocks.append([symbol, details['name'], details['equity'], details['percent_change'], arrow])
    
df = pd.DataFrame(stocks, columns=("Symbol", "Name", "Current value", "Lifetime percent change", ""))
st.dataframe(df)


st.write("#### Balance sheet")

def load_and_clean_data(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, skiprows=2) 
    # Rename columns for easier access
    # Security	Top Level Legal Entity	Asset Class	Sub-Asset Class	Sub-Sub-Asset Class	Value	Quantity	% of Portfolio	Price Per Share (USD)	Adjusted Value (5/24/2023, USD)	Unfunded Commitment
    expected_columns = [
        "Security", "Top Level Legal Entity", "Asset Class", "Sub-Asset Class", 
        "Sub-Sub-Asset Class", "Value", "Quantity", "% of Portfolio", "Price Per Share (USD)", 
        "Adjusted Value (5/24/2023, USD)", "Unfunded Commitment"
    ]
    if len(df.columns) == len(expected_columns):
        df.columns = expected_columns
    else:
        st.error(f"Expected {len(expected_columns)} columns, but got {len(df.columns)}. Please check the structure of your Excel file.")
        return None

    # Drop any rows where the primary columns are NaN
    df = df.dropna(subset=["Security", "Value"])
    return df

# Load data
file_path = './data/BSSummary.xlsx'
dataframe = load_and_clean_data(file_path)

st.write("Summary of balance sheet:")
st.dataframe(dataframe)

