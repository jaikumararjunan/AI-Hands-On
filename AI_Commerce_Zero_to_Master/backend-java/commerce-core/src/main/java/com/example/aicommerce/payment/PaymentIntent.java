package com.example.aicommerce.payment;

import java.math.BigDecimal;
import java.time.Instant;

public record PaymentIntent(
        String paymentId,
        String orderId,
        BigDecimal amount,
        String currency,
        String paymentMethodRef,
        String gatewayReference,
        PaymentStatus status,
        BigDecimal refundedAmount,
        String nextAction,
        Instant createdAt,
        Instant updatedAt
) {}
