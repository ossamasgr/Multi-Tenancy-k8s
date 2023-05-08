from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import psycopg2
from kubernetes import client, config
import os
import subprocess


# Set up a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="109.123.248.14",
    port="31933",
    database="customers",
    user="postgres",
    password="GvRMLOYpg6"
)


cur = conn.cursor()
cur.execute(
    "SELECT company_name, contact_name, contact_email, password FROM customers")
customers = cur.fetchall()
cur.close()
for customer in customers:
    print(customer)

