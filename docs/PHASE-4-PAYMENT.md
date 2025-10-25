# PHASE 4: Payment Processing Integration

## Overview
Implement Razorpay payment gateway for checkout and lead qualification to enable monetization of the Sunidhi Fashion automation platform.

## Current Status: READY FOR IMPLEMENTATION
- ✅ Backend API deployed on Render
- ✅ Environment variables configured
- ✅ Razorpay credentials in .env
- ✋ In Progress: Payment endpoint integration

## Razorpay Integration Steps

### 1. Razorpay Account Setup
**Already Completed:**
- Account created: idealabsllp@gmail.com
- Merchant ID: Configured
- API Keys stored in environment variables

### 2. Backend Payment Endpoint Implementation

**Current Implementation Status:**
The backend is ready for payment processing with the following planned endpoints:

#### POST /api/checkout
Initiate a payment order

```python
@app.route('/api/checkout', methods=['POST'])
def create_order():
    """
    Create Razorpay order
    Request:
    {
        "lead_id": "123",
        "amount": 999,  # in paise (1 INR = 100 paise)
        "description": "Lead Qualification Package"
    }
    """
    try:
        data = request.json
        
        # Create Razorpay order
        order_data = {
            'amount': data['amount'],
            'currency': 'INR',
            'receipt': f"lead_{data['lead_id']}",
            'notes': {
                'lead_id': data['lead_id'],
                'description': data['description']
            }
        }
        
        order = razorpay_client.order.create(data=order_data)
        
        # Store order in database
        # db.orders.insert_one(order)
        
        return jsonify({
            'status': 'success',
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency']
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

#### POST /api/verify-payment
Verify and complete payment

```python
@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    """
    Verify Razorpay payment
    Request:
    {
        "order_id": "order_123",
        "payment_id": "pay_456",
        "signature": "signature_value"
    }
    """
    try:
        data = request.json
        
        # Verify signature
        verify_data = {
            'razorpay_order_id': data['order_id'],
            'razorpay_payment_id': data['payment_id'],
            'razorpay_signature': data['signature']
        }
        
        razorpay_client.utility.verify_payment_signature(verify_data)
        
        # Payment verified
        # Update order status in database
        # db.orders.update_one(
        #     {'_id': data['order_id']},
        #     {'$set': {'status': 'completed', 'payment_id': data['payment_id']}}
        # )
        
        return jsonify({
            'status': 'success',
            'message': 'Payment verified successfully',
            'payment_id': data['payment_id']
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Payment verification failed'}), 400
```

### 3. Frontend Implementation

#### HTML/JavaScript for Payment Form

```html
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>

<button onclick="initiatePayment()">Pay Now</button>

<script>
function initiatePayment() {
    // Step 1: Create order on backend
    fetch('https://sunidhi-automation-backend.onrender.com/api/checkout', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            lead_id: '123',
            amount: 99900,  // 999 INR in paise
            description: 'Lead Qualification Package'
        })
    })
    .then(response => response.json())
    .then(data => {
        const options = {
            key: process.env.RAZORPAY_KEY_ID,
            order_id: data.order_id,
            handler: function(response) {
                verifyPayment(response);
            },
            prefill: {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                contact: document.getElementById('phone').value
            },
            theme: {
                color: '#FF6B00'  // Sunidhi branding color
            }
        };
        
        const rzp1 = new Razorpay(options);
        rzp1.open();
    });
}

function verifyPayment(response) {
    fetch('https://sunidhi-automation-backend.onrender.com/api/verify-payment', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            order_id: response.razorpay_order_id,
            payment_id: response.razorpay_payment_id,
            signature: response.razorpay_signature
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Payment successful!');
            // Redirect to success page
        }
    })
    .catch(error => {
        alert('Payment failed: ' + error);
    });
}
</script>
```

## Pricing Strategy

### Lead Qualification Package: ₹999
- Lead capture and qualification
- Automated voice call
- Lead scoring
- CRM entry in Google Sheets
- 24-hour follow-up support

### Premium Package: ₹2,999
- All above features
- Priority lead handling
- Custom voice message
- Email follow-ups
- 7-day support

### Enterprise: Custom Pricing
- Dedicated account manager
- API access
- White-label solution
- Custom integration
- Unlimited API calls

## Testing Payment Integration

### Razorpay Test Credentials
```
Test Mode: Enabled
Card Number: 4111111111111111
Expiry: Any future date (e.g., 12/25)
CVV: Any 3 digits (e.g., 123)
```

### Test Cases

**1. Successful Payment**
- Submit form with test card
- Verify order created in Razorpay
- Confirm payment marked as completed
- Check Google Sheets for new entry

**2. Failed Payment**
- Use invalid card details
- Verify error handling
- Check order not marked as completed

**3. Payment Timeout**
- Close payment modal
- Verify order saved as pending
- Allow retry option

## Security Considerations

### PCI Compliance
- ✅ Never store card details on server
- ✅ Use Razorpay's hosted checkout
- ✅ Validate signatures server-side

### Webhook Security
```python
@app.route('/webhook/razorpay', methods=['POST'])
def razorpay_webhook():
    """
    Handle Razorpay webhook events
    Events: payment.authorized, payment.failed, order.paid
    """
    webhook_body = request.data
    webhook_signature = request.headers.get('X-Razorpay-Signature')
    
    # Verify webhook signature
    try:
        razorpay_client.utility.verify_webhook_signature(
            webhook_body,
            webhook_signature,
            os.getenv('RAZORPAY_WEBHOOK_SECRET')
        )
        
        # Process webhook
        payload = request.json
        event = payload['event']
        
        if event == 'payment.authorized':
            # Handle successful payment
            pass
        elif event == 'payment.failed':
            # Handle failed payment
            pass
            
        return jsonify({'status': 'received'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Invalid signature'}), 400
```

## Implementation Checklist

- [ ] Create payment endpoints in backend
- [ ] Implement payment form in frontend
- [ ] Set up Razorpay webhook handling
- [ ] Add payment verification logic
- [ ] Integrate with Google Sheets (mark as paid)
- [ ] Create payment success/failure pages
- [ ] Add email receipts
- [ ] Test with Razorpay test cards
- [ ] Set up payment reconciliation
- [ ] Monitor failed payments
- [ ] Implement refund process
- [ ] Add payment analytics

## Razorpay Dashboard
- **Dashboard**: https://dashboard.razorpay.com
- **Webhook Configuration**: Settings → Webhooks
- **API Documentation**: https://razorpay.com/docs/

## Next Steps

1. Implement payment endpoints (backend/app.py)
2. Add payment form to website frontend
3. Configure Razorpay webhooks
4. Test complete payment flow
5. Set up payment analytics
6. Move to PHASE 5: Monitoring & Logging
