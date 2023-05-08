#Helm Chart for Workflow Applicaton 
### What is helm chart ?
A Helm chart is a set of YAML manifests and templates that describes Kubernetes resources (Deployments, Secrets, CRDs, etc.) and defined configurations needed for the Kubernetes application

### This helm chart contains :
- Chart for Front-end 
- Chart for Backend-app
- Chart for MySQL Database

the helm chart will deploy the database first and waits until it's ready then deploys the application 

### how to test the chart ?

```bash
company_name={the name of the comapany}

helm install $company_name Helm-Workflow-App/ -n $company_name --create-namespace --set mysql.auth.database="$company_name",workflow-backend.company_name=$company_name,workflow-frontend.company_name=$company_name
```
- -n : the namespace of kuberntes
- mysql.auth.database : it will name the mysql database according to the company name
- workflow-backend.company_name : it will set the backend name as the company name 
- workflow-frontend.company_name : it will set the backend name as the company name 

