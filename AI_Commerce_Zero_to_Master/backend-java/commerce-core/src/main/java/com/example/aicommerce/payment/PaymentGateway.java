package com.example.aicommerce.payment;

import java.math.BigDecimal;

/**
 * Provider-neutral payment port. A Stripe/Adyen/PayPal adapter can implement this interface.
 * Never accept raw PAN/CVV in this service; use provider tokens/payment-method references.
 */
public interface PaymentGateway {
    GatewayResult create(String orderId, BigDecimal amount, String currency,
                         String paymentMethodRef, String idempotencyKey);
    GatewayResult confirm(String gatewayReference);
    GatewayResult capture(String gatewayReference, BigDecimal amount);
    GatewayResult refund(String gatewayReference, BigDecimal amount);
}
