# Gateway-App

The Gateway app is a multi-tenant web application designed to provide a seamless experience for users to register and create their own dedicated Helm Chart application on a Kubernetes cluster. The app provides a simple and intuitive user interface that allows users to enter their registration details, such as name, email, and company, and then automatically creates a new Helm Chart application for them. The application architecture is designed to be highly scalable and secure, ensuring that each user's data is kept separate and confidential.# To Test the app 

# Architecture : 
![ProcessNavigation app](https://user-images.githubusercontent.com/59144753/236779560-d5da363e-bfbc-4679-9268-d4df2111f1df.png)

### Workflow  
- A user access the Gateway registration form 
- The user enters the company information and send the request
- the gateway app takes the arguments and creates the helm application
- after the application is created the user is redirected to the login page so they can access their app


**Home Page**
![image.png](./image.png)

**to register a new client**
![image-1.png](./image-1.png)

**to login with new client**
![image-2.png](./image-2.png)

**to Delete clients**
![image-3.png](./image-3.png)


