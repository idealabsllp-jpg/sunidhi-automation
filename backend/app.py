from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Health check endpoint (for Render to keep app alive)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Sunidhi Automation is running!"})

# OmniDimension webhook (receives voice call data)
@app.route("/omnidim-webhook", methods=["POST"])
def omnidim_webhook():
    try:
        data = request.form.to_dict() or request.get_json()
        print(f"Received OmniDimension data: {data}")
        return jsonify({"status": "received"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 400

# Payment webhook (from Razorpay - optional for MVP)
@app.route("/razorpay-webhook", methods=["POST"])
def razorpay_webhook():
    try:
        data = request.get_json()
        print(f"Payment received: {data}")
        return ("", 204)
    except Exception as e:
        print(f"Payment error: {e}")
        return ("", 400)

# Lead form submission endpoint
@app.route("/submit-lead", methods=["POST"])
def submit_lead():
    try:
        data = request.get_json()
        name = data.get("name")
        phone = data.get("phone")
        product = data.get("product")
        print(f"New lead: {name}, {phone}, interested in {product}")
        return jsonify({"status": "success", "message": "Lead saved!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# PHASE 4: Payment Processing Endpoints
import razorpay

razorpay_client = razorpay.Client(auth=(os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRET')))

@app.route('/api/checkout', methods=['POST'])
def create_order():
    """Create Razorpay payment order for lead qualification"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('lead_id') or not data.get('amount'):
            return jsonify({'error': 'Missing lead_id or amount'}), 400
        
        # Create Razorpay order
        order_data = {
            'amount': int(data.get('amount')),  # Amount in paise (1 INR = 100 paise)
            'currency': 'INR',
            'receipt': f"lead_{data.get('lead_id')}",
            'notes': {
                'lead_id': data.get('lead_id'),
                'description': data.get('description', 'Lead Qualification Package')
            }
        }
        
        order = razorpay_client.order.create(data=order_data)
        
        print(f"Order created: {order['id']} for lead: {data.get('lead_id')}")
        
        return jsonify({
            'status': 'success',
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency'],
            'key': os.getenv('RAZORPAY_KEY_ID')
        }), 201
        
    except Exception as e:
        print(f"Error creating order: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    """Verify Razorpay payment signature"""
    try:
        data = request.get_json()
        
        # Verify payment signature
        verify_data = {
            'razorpay_order_id': data.get('order_id'),
            'razorpay_payment_id': data.get('payment_id'),
            'razorpay_signature': data.get('signature')
        }
        
        razorpay_client.utility.verify_payment_signature(verify_data)
        
        print(f"Payment verified: {data.get('payment_id')}")
        
        return jsonify({
            'status': 'success',
            'message': 'Payment verified successfully',
            'payment_id': data.get('payment_id')
        }), 200
        
    except razorpay.BadRequestsError as e:
        print(f"Payment verification failed: {e}")
        return jsonify({'error': 'Payment verification failed', 'details': str(e)}), 400
    except Exception as e:
        print(f"Error verifying payment: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/payment-status/<payment_id>', methods=['GET'])
def get_payment_status(payment_id):
    """Get payment status from Razorpay"""
    try:
        payment = razorpay_client.payment.fetch(payment_id)
        
        return jsonify({
            'status': payment['status'],
            'amount': payment['amount'],
            'currency': payment['currency'],
            'method': payment.get('method'),
            'created_at': payment.get('created_at')
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
