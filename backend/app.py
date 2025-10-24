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
        
        # Store call data (you can save to Google Sheets later)
        # For now, just acknowledge receipt
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
        
        # You'll add Google Sheets integration here later
        return jsonify({"status": "success", "message": "Lead saved!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

  Add Flask backend app.py
