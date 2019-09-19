# Steps to setup AKS with Azure CNI 
pre-requisits azure shell az is installed logged in to az account, by doing `az login` 

###  Environment set up 
##### Echo the variables
```sh
export SUBSCRIPTION_ID='*********'
export SUBSCRIPTION_NAME='********'
export RESOURCE_GROUP_NAME='vibhoreTest' 
export LOCATION='eastus'
export AKS_CLUSTER_NAME='vibhoreTestAKS' 
export SSH_PUB_KEY='********' 
export K8S_VERSION='1.14.6'
export TENANT_ID='****'
export VNET_NAME='K8STestVnet'
export SUBNET_NAME='VibhoreTestAKSSubnet' 
```

##### Set default subscription 
```sh
az account set --subscription $SUBSCRIPTION_NAME
```

##### Create resource group if not already created 
```sh
az group create --name $RESOURCE_GROUP_NAME  --location $LOCATION
```

### Networking

Currently we are using azure CNI for networking, so we need to plan for ip subnets, & get into details like:
 * how many services we are expecting
 * what is the max no of pods we may need in next 1 year for those services
 * no of ip per node
 * max pod per node 

refer: https://docs.microsoft.com/en-us/azure/aks/configure-azure-cni
      
##### Vnet & Subnet 
```sh
# Create vnet and subnet, if not already  or use an existing vnet 
az network vnet create \
    --resource-group $RESOURCE_GROUP_NAME \
    --name TestAKSVnet \
    --address-prefixes 192.168.0.0/16 \
    --subnet-name $SUBNET_NAME \
    --subnet-prefix 192.168.1.0/24


# Create subnet if vnet is already there 
az network vnet subnet create -g $RESOURCE_GROUP_NAME --vnet-name $VNET_NAME -n $SUBNET_NAME \
    --address-prefixes 10.0.0.0/24 --network-security-group <if applicable>  --route-table <if applicable> 
```

### Service principal

Create service principal if not already there for the resource group.
The service principal needs to have permissions to manage the virtual network and subnet that the AKS nodes use.
 
##### Export vnet id & Subnet id created in previous step or the existing ones you are using 
```sh
export VNET_ID='*******'
export SUBNET_ID='********'
```

##### Create service principal with role assignment
```sh
# Ex Command: 
az ad sp create-for-rbac -n "MyApp" --role contributor \
  --scopes /subscriptions/{SubID}/resourceGroups/{ResourceGroup1} \
    /subscriptions/{SubID}/resourceGroups/{ResourceGroup2}
```
```sh
# Permission for Subnet is not required vpn permission is enough
az ad sp create-for-rbac -n "TestK8sApp" --role contributor \
    --scopes $VNET_ID
```

### Create aks cluster
##### Export client id  & secret of sp created in last step
```sh
export SP_CLIENT_ID='*****'
export SP_SECRET='*****'
```
##### To setup aks with azure cni, it is imp to pass these parameters, these are not compulsory but critical when setting up for prod environment. One needs to figure out free CIDR(s) for these. 
    1. docker-bridge-address 172.17.0.1/16  # cidr that does not collide with the rest of the CIDRs on your networks
    2. dns-service-ip 10.2.0.10. IP address in your service-cidr address range, but not the 1st ip of range
    3. service-cidr 10.2.0.0/24  # ips which should not concide with virtual n/w of aks & any other n/w it connects to 
        also should not concide with 169.254.0.0/16, 172.30.0.0/16, 172.31.0.0/16, oC 192.0.2.0/24
##### Create cluster without essential subnet ranges (without above mentioned cidr params)
```sh
az aks create -g $RESOURCE_GROUP_NAME -n $AKS_CLUSTER_NAME --ssh-key-value $SSH_PUB_KEY --node-count 1 --enable-addons monitoring \
   --vnet-subnet-id  $SUBNET_ID\
   --kubernetes-version $K8S_VERSION --node-vm-size Standard_DS2_v2  --nodepool-name team1 --network-plugin azure --service-principal $SP_CLIENT_ID \
   --client-secret $SP_SECRET --tags 'environment=dev' 'product=ares' 'team=team1' 'service=service1'

```

