subscription_id = ""
management_group_id = "test"
resource_group_name  = "rg_script"
############vnet############
vnet_name = 'testvnet'
vnet_cidr = "10.0.0.0/16"

# az command to get the id "az role definition list --query "[?roleName=='Contributor'].{Name:roleName, Id:id}""


############Tags for subscription############
tags =  {
    'env': 'dev',
    'test': 'test1'
    }

############Service Principal############
client_id = ''
tenant_id = ''

role_definition_id_sp = "" #use the following command to get the contributor id
# az command to get the id "az role definition list --query "[?roleName=='Contributor'].{Name:roleName, Id:id}

principal_id_sp = '' #use the following command to get the principal id
#az ad sp list --filter "displayName eq 'sp_name'"
scope_sp = '/subscriptions/' + subscription_id
