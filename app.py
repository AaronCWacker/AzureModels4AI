import streamlit as st
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os
import pandas as pd
import traceback  # For detailed error stacks

st.set_page_config(layout="wide")

# Cosmos DB configuration
ENDPOINT = "https://acae-afd.documents.azure.com:443/"
SUBSCRIPTION_ID = "003fba60-5b3f-48f4-ab36-3ed11bc40816"
DATABASE_NAME = os.environ.get("COSMOS_DATABASE_NAME")
CONTAINER_NAME = os.environ.get("COSMOS_CONTAINER_NAME")
Key = os.environ.get("Key")

def insert_record(record):
    try:
        response = container.create_item(body=record)
        return True, response
    except exceptions.CosmosHttpResponseError as e:
        return False, f"HTTP error occurred: {str(e)}. Status code: {e.status_code}"
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"

def call_stored_procedure(record):
    try:
        response = container.scripts.execute_stored_procedure(
            sproc="processPrompt",
            params=[record],
            partition_key=record['id']
        )
        return True, response
    except exceptions.CosmosHttpResponseError as e:
        error_message = f"HTTP error occurred: {str(e)}. Status code: {e.status_code}"
        return False, error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return False, error_message

def fetch_all_records():
    try:
        query = "SELECT * FROM c"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return pd.DataFrame(items)
    except exceptions.CosmosHttpResponseError as e:
        st.error(f"HTTP error occurred while fetching records: {str(e)}. Status code: {e.status_code}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An unexpected error occurred while fetching records: {str(e)}")
        return pd.DataFrame()

def update_record(updated_record):
    try:
        container.upsert_item(body=updated_record)  # Upsert updates the item if it exists
        return True, f"Record with id {updated_record['id']} successfully updated."
    except exceptions.CosmosHttpResponseError as e:
        return False, f"HTTP error occurred: {str(e)}. Status code: {e.status_code}"
    except Exception as e:
        return False, f"An unexpected error occurred: {traceback.format_exc()}"

def delete_record(name, id):
    try:
        container.delete_item(item=id, partition_key=id)
        return True, f"Successfully deleted record with name: {name} and id: {id}"
    except exceptions.CosmosResourceNotFoundError:
        return False, f"Record with id {id} not found. It may have been already deleted."
    except exceptions.CosmosHttpResponseError as e:
        return False, f"HTTP error occurred: {str(e)}. Status code: {e.status_code}"
    except Exception as e:
        return False, f"An unexpected error occurred: {traceback.format_exc()}"

# Streamlit app
st.title("🌟 Cosmos DB Record Management")

# Initialize session state for selected records
if 'selected_records' not in st.session_state:
    st.session_state.selected_records = []

# Login section
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    input_key = Key  # Use the predefined Key instead of asking for user input
    if st.button("🚀 Login"):
        if input_key:
            st.session_state.primary_key = input_key
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid key. Please check your environment variables.")
else:
    # Initialize Cosmos DB client
    try:
        client = CosmosClient(ENDPOINT, credential=st.session_state.primary_key)
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)
    except exceptions.CosmosHttpResponseError as e:
        st.error(f"Failed to connect to Cosmos DB. HTTP error: {str(e)}. Status code: {e.status_code}")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred while connecting to Cosmos DB: {str(e)}")
        st.stop()

    # Fetch and display all records
    st.subheader("📊 All Records")
    df = fetch_all_records()

    if df.empty:
        st.write("No records found in the database.")
    else:
        st.write("Records:")
        for index, row in df.iterrows():
            col1, col2, col3 = st.columns([5, 1, 1])

            with col1:
                # Display all fields in the listing
                st.write(f"ID: {row['id']}, Name: {row['name']}, Document: {row['document']}, "
                         f"Evaluation Text: {row['evaluationText']}, Evaluation Score: {row['evaluationScore']}")

            with col2:
                key = f"select_{row['id']}"
                if st.button(f"👉 Select", key=key):
                    st.session_state.selected_record = row.to_dict()

            with col3:
                if st.button(f"🗑️ Delete", key=f"delete_{row['id']}"):
                    success, message = delete_record(row['name'], row['id'])
                    if success:
                        st.success(message)
                        st.rerun()  # Refresh after deletion
                    else:
                        st.error(message)

    # Display selected record for editing
    if 'selected_record' in st.session_state and st.session_state.selected_record:
        selected_record = st.session_state.selected_record

        st.subheader(f"Editing Record - ID: {selected_record['id']}")

        # Editable fields prefilled with the selected record
        updated_name = st.text_input("Name", value=selected_record['name'])
        updated_document = st.text_area("Document", value=selected_record['document'])
        updated_evaluation_text = st.text_area("Evaluation Text", value=selected_record['evaluationText'])
        updated_evaluation_score = st.text_input("Evaluation Score", value=str(selected_record['evaluationScore']))

        # Update button with emoji
        if st.button("💾 Save Changes"):
            updated_record = {
                "id": selected_record['id'],
                "name": updated_name,
                "document": updated_document,
                "evaluationText": updated_evaluation_text,
                "evaluationScore": updated_evaluation_score  # Now treated as a string
            }

            success, message = update_record(updated_record)
            if success:
                st.success(message)
                st.session_state.selected_record = updated_record  # Update the session state with new values
            else:
                st.error(message)

    # Input fields for new record
    st.subheader("📝 Enter New Record Details")
    new_id = st.text_input("ID")
    new_name = st.text_input("Name")
    new_document = st.text_area("Document")
    new_evaluation_text = st.text_area("Evaluation Text")
    new_evaluation_score = st.text_input("Evaluation Score")  # Now treated as a string

    col1, col2 = st.columns(2)

    # Insert Record button
    with col1:
        if st.button("💾 Insert Record"):
            record = {
                "id": new_id,
                "name": new_name,
                "document": new_document,
                "evaluationText": new_evaluation_text,
                "evaluationScore": new_evaluation_score  # Insert as a string
            }

            success, response = insert_record(record)
            if success:
                st.success("✅ Record inserted successfully!")
                st.json(response)
            else:
                st.error(f"❌ Failed to insert record: {response}")
            st.rerun()

    # Call Procedure button
    with col2:
        if st.button("🔧 Call Procedure"):
            record = {
                "id": new_id,
                "name": new_name,
                "document": new_document,
                "evaluationText": new_evaluation_text,
                "evaluationScore": new_evaluation_score
            }

            success, response = call_stored_procedure(record)
            if success:
                st.success("✅ Stored procedure executed successfully!")
                st.json(response)
            else:
                st.error(f"❌ Failed to execute stored procedure: {response}")

    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.selected_records.clear()  # Clear selected records on logout
        st.session_state.selected_record = None  # Clear selected record
        st.rerun()

    # Display connection info
    st.sidebar.subheader("🔗 Connection Information")
    st.sidebar.text(f"Endpoint: {ENDPOINT}")
    st.sidebar.text(f"Subscription ID: {SUBSCRIPTION_ID}")
    st.sidebar.text(f"Database: {DATABASE_NAME}")
    st.sidebar.text(f"Container: {CONTAINER_NAME}")
