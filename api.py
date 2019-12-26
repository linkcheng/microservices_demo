#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@sfy.com
@module: api 
@date: 2018-12-14
 http://localhost:5000/apidocs
 http://localhost:5000/apidocs/#/default/post_compute
"""
from flask import Flask, request
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


@app.route('/compute', methods=['POST'])
def compute():
    """
    Micro Service Based Compute and Mail API
    This API is made with Flask, Flasgger and Nameko
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: data
          properties:
            operation:
              type: string
              enum:
                - sum
                - mul
                - sub
                - div
            email:
              type: string
            value:
              type: integer
            other:
              type: integer
    responses:
      200:
        description: Please wait the calculation, you'll receive an email with results
    """
    operation = request.json.get('operation')
    value = request.json.get('value')
    other = request.json.get('other')
    email = request.json.get('email')
    msg = "Please wait the calculation, you'll receive an email with results"
    subject = "API Notification"

    with ClusterRpcProxy(CONFIG) as rpc:
        # asynchronously spawning and email notification
        rpc.mail.send.call_async(email, subject, msg)
        # asynchronously spawning the compute task
        rpc.compute.compute.call_async(operation, value, other, email)

    return msg, 200


if __name__ == '__main__':
    app.run(debug=True)
