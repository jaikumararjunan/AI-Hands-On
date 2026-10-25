package com.example.aicommerce.payment;

public record GatewayResult(
        String gatewayReference,
        PaymentStatus status,
        String nextAction
) {}
