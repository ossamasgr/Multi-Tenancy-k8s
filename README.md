# Gateway-App

# To Test the app 
URL : https://gateway.rifnology.com/
![image.png](./image.png)
to register a new client : https://gateway.rifnology.com/register
![image-1.png](./image-1.png)
to login with new client : https://gateway.rifnology.com/login
![image-2.png](./image-2.png)
to Delete clients : https://gateway.rifnology.com/admin
![image-3.png](./image-3.png)


# to create a user : 

```
curl -X 'POST' \
'https://{companyname}.rifnology.com/api/users/registration' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
"name": "Jhon Doe",
"email": "example@mail.mail",
"role": "Admin",
"status": "Active",
"password": "password"
}'

```
