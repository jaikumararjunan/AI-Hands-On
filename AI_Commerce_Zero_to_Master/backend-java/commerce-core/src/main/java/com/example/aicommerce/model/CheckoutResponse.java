package com.example.aicommerce.model;

import com.example.aicommerce.payment.PaymentIntent;

public record CheckoutResponse(Order order, PaymentIntent payment) {}
