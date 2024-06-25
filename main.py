import logging
from flask import Flask, request, jsonify
from pyaadhaar.decode import AadhaarSecureQr

app = Flask(__name__)

@app.route('/qr_trigger', methods=['GET', 'POST'])
def qr_trigger():
    logging.info('Python HTTP trigger function processed a request.')

    if request.method == 'GET':
        encrypted_qr_data = request.args.get('data')
    elif request.method == 'POST':
        req_body = request.get_json()
        encrypted_qr_data = req_body.get('data')

    if encrypted_qr_data:
        try:
            encrypted_qr_data_int = int(encrypted_qr_data)
            obj = AadhaarSecureQr(encrypted_qr_data_int)
            decoded_data = obj.decodeddata()
            success_message = {"success": "Decoding successful", "result": decoded_data}
            return jsonify(success_message), 200
        except Exception as e:
            logging.error(f"Error decoding Aadhaar QR: {str(e)}")
            error_message = {"error": "Internal Server Error"}
            return jsonify(error_message), 500
    else:
        error_message = {"error": "Bad Request: 'data' parameter is missing"}
        return jsonify(error_message), 400

def handler(event, context):
    with app.test_request_context(
            method=event['httpMethod'],
            path=event['path'],
            query_string=event['queryStringParameters'],
            headers=event['headers'],
            data=event['body']):
        return app.full_dispatch_request().get_data()
