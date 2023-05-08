from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import psycopg2
from kubernetes import client, config
import os
import subprocess
import time

# Load configuration from kubeconfig file or environment variables
config.load_incluster_config()
#config.load_kube_config()

# Create Kubernetes API client
v1 = client.CoreV1Api()
api = client.AppsV1Api()
postgres_host = os.getenv("POSTGRES_HOST")
postgres_password = os.getenv("POSTGRES_PASSWORD")
# Set up a connection to the PostgreSQL database
conn = psycopg2.connect(
    host=postgres_host,
    port="5432",
    database="customers",
    user="postgres",
    password=postgres_password
)

app = Flask(__name__)
app.secret_key = 'mysecretkey'
# Close the connection to the PostgreSQL database after each request


@app.route('/register')
def index():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    company_name = request.form['company_name']
    contact_name = request.form['contact_name']
    contact_email = request.form['contact_email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    subdomain = company_name.lower()
    # if password don't match
    if password != confirm_password:
        error = 'Passwords do not match.'
        return render_template('register.html', error=error)

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Check if the customer already exists
    cur.execute(
        "SELECT company_name  FROM customers  WHERE company_name =  %s", (subdomain,))

    # Fetch the results and print them
    result = cur.fetchone()
    if result:
        return (f"Sorry but The company {subdomain} already exists, Please Login or contact your adminstrator")
    else:
        # Insert a new row into the customers table
        cur.execute("INSERT INTO customers (company_name, contact_name, contact_email, password) VALUES (%s, %s, %s, %s)",
                    (company_name, contact_name, contact_email, password))
        conn.commit()

        # Deploy the client's app to their namespace
        command = ["helm", "install", subdomain, "Helm-Workflow-App/",
                   "-n", subdomain, "--create-namespace",
                   "--set", f"mysql.auth.database={subdomain}",
                   "--set", f"workflow-backend.company_name={subdomain}",
                   "--set", f"workflow-frontend.company_name={subdomain}"]

        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Return login page
        return render_template('wait.html', subdomain=subdomain)

@app.route('/login')
def login_redirect():
    return render_template('login.html')

@app.route('/status/<subdomain>')
def status(subdomain):
    sts = api.read_namespaced_stateful_set(
        name=f"{subdomain}-mysql", namespace=subdomain)
    dep_front = api.read_namespaced_deployment(
        name=f"{subdomain}-workflow-frontend", namespace=subdomain)
    dep_back = api.read_namespaced_deployment(
        name=f"{subdomain}-workflow-backend", namespace=subdomain)

    ready = (sts.status.ready_replicas == sts.status.replicas and
             dep_front.status.ready_replicas == dep_front.status.replicas and
             dep_back.status.ready_replicas == dep_back.status.replicas)

    return jsonify({'ready': ready})


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    app_url = hostname
    full_url = 'https://' + app_url + '/' +  username

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    cur.execute(
        "SELECT company_name, password FROM customers WHERE company_name = %s", (username,))
    # Fetch the results and print them
    result = cur.fetchone()
    if result:
        db_password = result[1]
        if password == db_password:
            return redirect(full_url)
        else:
            #Continued from previous message...

            # Password is incorrect, add a message to the session and redirect to the login page
            error = 'Invalid password'
            return render_template('login.html', error=error)
    else:

        error = f"Sorry but The company {username} doesn't exist, Please Register or contact your administrator"
        return render_template('login.html', error=error)


@app.route('/admin')
def admin_customers():
    # Query the customers table
    cur = conn.cursor()
    cur.execute(
        "SELECT company_name, contact_name, contact_email FROM customers")
    data = cur.fetchall()
    cur.close()

    return render_template('admin.html', data=data)


@app.route('/delete/<company_name>', methods=['POST'])
def delete_customer(company_name):
    try:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM customers WHERE company_name = %s;", (company_name,))
        conn.commit()
        # delete the client's app to their namespace
        command = ["helm", "delete", company_name,
                   "--namespace", company_name]
        # Delete the namespace
        v1.delete_namespace(company_name, body=client.V1DeleteOptions())

        flash('Customer deleted successfully!')
    except (Exception, psycopg2.Error) as error:
        print(error)
        flash('An error occurred while deleting the customer.')

    return redirect(url_for('admin_customers'))


@app.route('/')
def home_red():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

