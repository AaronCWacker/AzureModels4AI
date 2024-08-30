import streamlit as st
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.cosmos import CosmosClient

def create_resource_group(credential, subscription_id, resource_group_name, location):
    resource_client = ResourceManagementClient(credential, subscription_id)
    rg_result = resource_client.resource_groups.create_or_update(
        resource_group_name,
        {"location": location}
    )
    return rg_result

def create_cosmos_account(credential, subscription_id, resource_group_name, account_name, location):
    cosmos_client = CosmosDBManagementClient(credential, subscription_id)
    poller = cosmos_client.database_accounts.begin_create_or_update(
        resource_group_name,
        account_name,
        {
            "location": location,
            "locations": [{"locationName": location}],
            "database_account_offer_type": "Standard"
        }
    )
    account_result = poller.result()
    return account_result

def main():
    st.title("Azure CosmosDB Creator")
    
    # Input parameters
    tenant_id = st.text_input("Azure Tenant ID")
    client_id = st.text_input("Azure Client ID")
    client_secret = st.text_input("Azure Client Secret", type="password")
    subscription_id = st.text_input("Azure Subscription ID")
    
    resource_group_name = st.text_input("Resource Group Name")
    location = st.text_input("Location", value="eastus")
    account_name = st.text_input("CosmosDB Account Name")
    
    if st.button("Create CosmosDB"):
        try:
            # Create credential object
            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
            
            # Create Resource Group
            st.write("Creating Resource Group...")
            rg_result = create_resource_group(credential, subscription_id, resource_group_name, location)
            st.write(f"Resource Group '{rg_result.name}' created successfully.")
            
            # Create CosmosDB Account
            st.write("Creating CosmosDB Account...")
            cosmos_result = create_cosmos_account(credential, subscription_id, resource_group_name, account_name, location)
            st.write(f"CosmosDB Account '{cosmos_result.name}' created successfully.")
            
            # Display connection information
            st.success("CosmosDB resource created successfully!")
            st.write("Connection Information:")
            st.write(f"Endpoint: {cosmos_result.document_endpoint}")
            st.write(f"Primary Key: {cosmos_result.read_write_database_account_keys.primary_master_key}")
            
            # Example of how to use the created CosmosDB
            st.write("\nExample usage:")
            st.code("""
# Connect to your CosmosDB account
from azure.cosmos import CosmosClient

endpoint = "{cosmos_result.document_endpoint}"
key = "{cosmos_result.read_write_database_account_keys.primary_master_key}"

client = CosmosClient(endpoint, key)

# Create a database
database_name = "my-database"
database = client.create_database_if_not_exists(id=database_name)

# Create a container
container_name = "my-container"
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key="/partitionKey",
    offer_throughput=400
)

# Create an item
item = {
    "id": "item1",
    "partitionKey": "value1",
    "description": "This is a sample item"
}
container.create_item(body=item)

# Query items
query = "SELECT * FROM c WHERE c.partitionKey = 'value1'"
items = list(container.query_items(query=query, enable_cross_partition_query=True))
for item in items:
    print(item)
            """)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()