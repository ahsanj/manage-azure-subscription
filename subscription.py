#!/usr/bin/env python3
import config
import sys
from azure.mgmt.managementgroups import ManagementGroupsAPI
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.subscriptions import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import AddressSpace , VirtualNetwork

# class AzureCredentials:
#     def __init__(self):
#         self.credential = DefaultAzureCredential()

credential = AzureCliCredential()

def border_msg(msg):
    row = len(msg)
    h = ''.join(['+'] + ['-' *row] + ['+'])
    result= h + '\n'"|"+msg+"|"'\n' + h
    print(result)

def list_subscriptions():
    try:
        subscription_client = SubscriptionClient(credential)
        subscriptions = subscription_client.subscriptions.list()
        for sub in subscriptions:
            border_msg(f"Name: {sub.display_name} ID: {sub.subscription_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def move_subscription():
    try:
        print("Enabling the SecurityInsights before moving the subscription")
        enable_resource_provider()
        mgmt_group_client = ManagementGroupsAPI(credential)
        mgmt_group_client.management_group_subscriptions.create(group_id=config.management_group_id,
                                                                subscription_id=config.subscription_id)
        print('Subscription {} has been moved to management group {}.'.format(config.subscription_id, config.management_group_id))       
    except Exception as e:
        print(f"An error occurred: {e}")

def enable_resource_provider():
    try:
        resource_client = ResourceManagementClient(credential,config.subscription_id)
        resource_provider = 'Microsoft.SecurityInsights'
        resource_client.providers.register(resource_provider)
    except Exception as e:
        print(f"An error occurred: {e}")
    
def create_vnet():
    try:
        resource_group_name = config.resource_group_name 
        vnet_name = config.vnet_name
        vnet_cidr = config.vnet_cidr
        network_client = NetworkManagementClient(credential=credential, subscription_id=config.subscription_id)
        
        vnet_params = VirtualNetwork(
        location="eastus",
        address_space=AddressSpace(
            address_prefixes=[vnet_cidr],
            ),
        )
        # if Resource provider 'Microsoft.Network' is not enabled the following operation will also enable it
        vnet_result = network_client.virtual_networks.begin_create_or_update(
        resource_group_name=resource_group_name,
        virtual_network_name=vnet_name,
        parameters=vnet_params,
        )
        print(f"Virtual network '{vnet_result.result().name}' created.")
    except Exception as e:
        print(f"An error occurred: {e}")
    

def create_resource_group():
    try:
        resource_client = ResourceManagementClient(credential, config.subscription_id)
        if resource_client.resource_groups.check_existence(config.resource_group_name):
            print("Resource group '{0}' already exists. Script stopped.".format(config.resource_group_name))
            exit()
        rg_result = resource_client.resource_groups.create_or_update(
        config.resource_group_name, {"location": "eastus"}
        )
        print(f"Provisioned resource group {rg_result.name} in the {rg_result.location} region")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def create_tags():
    pass

def assign_rbac_aad():
    pass

def assign_rbac_sp():
    pass
    
    
def main():
    
    def main_menu():
        print("Welcome to the Main Menu")
        print("1. List Subscriptions")
        print("2. Move Subscriptions ")
        print("3. Create Resource Group")
        print("4. Create Vnet")
        print("5. Create tags on the Subscription")
        print("6. Assign RBAC permisisons to AAD Group")
        print("7. Assign RBAC permisisons to Service principal")
        print("8. Exit")
        while True:
            try:
                choice = input("Enter your choice: ")
                choice = int(choice)
                if choice in range(1, 9):
                    return str(choice)
                else:
                    print("Invalid choice. Please enter a number between 1 and 8.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 8.")

    def list_sub():
        list_subscriptions()

    def move_sub():
        move_subscription()

    def resource_grp():
        create_resource_group()
    
    def vnet():
        create_vnet()
    
    def tag():
        create_tags()
    
    def assign_aad():
        assign_rbac_aad()
        
    def assign_sp():
        assign_rbac_sp()
        
    

    options = {
        "1": list_sub,
        "2": move_sub,
        "3": resource_grp,
        "4": vnet,
        "5": tag,
        "6": assign_aad,
        "7": assign_sp,
        "8": lambda: print("Exiting...")
    }

    while True:
        choice = main_menu()
        options.get(choice)()
        if choice == "8":
            break

if __name__ == "__main__":
    main()

