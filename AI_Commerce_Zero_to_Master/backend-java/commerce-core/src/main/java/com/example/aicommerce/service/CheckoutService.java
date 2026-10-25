package com.example.aicommerce.service;

import com.example.aicommerce.model.CheckoutRequest;
import com.example.aicommerce.model.CheckoutResponse;
import com.example.aicommerce.model.Order;
import com.example.aicommerce.model.PaymentIntentRequest;
import com.example.aicommerce.payment.PaymentIntent;
import com.example.aicommerce.payment.PaymentService;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Thin orchestration layer. Product price and discounts are calculated inside Java domain services.
 * The client supplies only cart/order intent and a tokenized payment-method reference.
 */
@Service
public class CheckoutService {
    private final OrderService orders;
    private final PaymentService payments;
    private final Map<String, CheckoutResponse> idempotencyIndex = new ConcurrentHashMap<>();

    public CheckoutService(OrderService orders, PaymentService payments) {
        this.orders = orders;
        this.payments = payments;
    }

    public synchronized CheckoutResponse checkout(CheckoutRequest request, String idempotencyKey) {
        CheckoutResponse existing = idempotencyIndex.get(idempotencyKey);
        if (existing != null) {
            return existing;
        }
        Order order = orders.create(request.order());
        PaymentIntent payment = payments.createIntent(
                new PaymentIntentRequest(order.orderId(), order.total(), request.currency(), request.paymentMethodRef()),
                "checkout:" + idempotencyKey
        );
        CheckoutResponse response = new CheckoutResponse(order, payment);
        idempotencyIndex.put(idempotencyKey, response);
        return response;
    }
}
