from paypalrestsdk import Payment, configure
import logging

def get_config(mode, client_id, client_secret):
    configure({
        "mode": mode,  # sandbox or live
        "client_id": client_id,
        "client_secret": client_secret
    })


def get_paypal_payment_url(amount_total, description_description="", base_url="", mode="live", client_id=None,
                           client_secret=None):
    get_config(mode, client_id, client_secret)
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        # Set redirect URLs
        "redirect_urls": {
            "return_url": base_url + "/payment/paypal/return",
            "cancel_url": base_url + "/payment/paypal/cancel"
        },

        # Set transaction object
        "transactions": [{
            "amount": {
                "total": amount_total,
                "currency": "USD"
            },
            "description": description_description
        }]
    })
    if payment.create():
        logging.info("payment.create, %s", payment)
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = (link.href)
                # print(redirect_url)
                return redirect_url
    else:
        logging.error("Error while creating payment: %s", payment)
    raise Exception("get paypal payment url error")
