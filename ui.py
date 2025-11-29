import streamlit as st
import requests

st.set_page_config(layout="wide")

st.title("🏦 Bank Management System")

BASE_URL = "http://127.0.0.1:8000" # Assuming FastAPI runs on this address

# --- Authentication Section ---
st.header("🔑 User Authentication")

with st.form("authentication_form"):
    auth_name = st.text_input("Username", key="auth_name")
    auth_pin_str = st.text_input("PIN Number", type="password", key="auth_pin")
    authenticate_button = st.form_submit_button("Authenticate")

    if authenticate_button:
        if not auth_name or not auth_pin_str:
            st.error("Please enter both username and PIN.")
        else:
            try:
                auth_pin = int(auth_pin_str.strip())
                response = requests.post(f"{BASE_URL}/authenticate", params={"name": auth_name, "pin_number": auth_pin})
                if response.status_code == 200 and "error" not in response.json():
                    st.success("Authentication successful!")
                    data = response.json()
                    st.json(data)
                    st.session_state["authenticated_user"] = auth_name
                    st.session_state["authenticated_pin"] = auth_pin
                    st.session_state["bank_balance"] = data.get("bank_balance")
                    
                else:
                    st.error("Authentication failed. Invalid credentials or server error.")
                    st.json(response.json())
            except ValueError:
                st.error("PIN must be a number.")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI server. Make sure it is running.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display current user info if authenticated
if "authenticated_user" in st.session_state and st.session_state["authenticated_user"]:
    st.sidebar.success(f"Logged in as: {st.session_state['authenticated_user']}")
    st.sidebar.info(f"Balance: ${st.session_state['bank_balance']:.2f}")

    if st.sidebar.button("Logout"):
        del st.session_state["authenticated_user"]
        del st.session_state["authenticated_pin"]
        del st.session_state["bank_balance"]
        

    # --- Deposit Section ---
    st.header("💸 Deposit Funds")
    with st.form("deposit_form"):
        deposit_amount = st.number_input("Amount to Deposit", min_value=0.01, format="%.2f", key="deposit_amount")
        deposit_button = st.form_submit_button("Deposit")

        if deposit_button:
            try:
                response = requests.post(
                    f"{BASE_URL}/deposit",
                    params={"name": st.session_state["authenticated_user"], "amount": deposit_amount}
                )
                if response.status_code == 200:
                    st.success("Deposit successful!")
                    st.json(response.json())
                    st.session_state["bank_balance"] = response.json().get("bank_balance")
                else:
                    st.error("Deposit failed.")
                    st.json(response.json())
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI server. Make sure it is running.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # --- Bank Transfer Section ---
    st.header("➡️ Bank Transfer")
    with st.form("bank_transfer_form"):
        recipient_name = st.text_input("Recipient Username", key="recipient_name")
        transfer_amount = st.number_input("Amount to Transfer", min_value=0.01, format="%.2f", key="transfer_amount")
        transfer_button = st.form_submit_button("Transfer")

        if transfer_button:
            if not recipient_name:
                st.error("Please enter a recipient username.")
            else:
                try:
                    response = requests.post(
                        f"{BASE_URL}/bank-transfer",
                        params={
                            "sender_name": st.session_state["authenticated_user"],
                            "sender_pin": st.session_state["authenticated_pin"],
                            "recipient_name": recipient_name,
                            "amount": transfer_amount
                        }
                    )
                    if response.status_code == 200:
                        st.success("Transfer successful!")
                        st.json(response.json())
                        # Update sender's balance in session state
                        st.session_state["bank_balance"] = response.json().get("sender_updated_balance")
                    else:
                        st.error("Transfer failed.")
                        st.json(response.json())
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to FastAPI server. Make sure it is running.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")