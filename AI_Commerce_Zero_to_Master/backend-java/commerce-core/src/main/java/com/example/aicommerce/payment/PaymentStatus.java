package com.example.aicommerce.payment;

public enum PaymentStatus {
    REQUIRES_ACTION,
    AUTHORIZED,
    PROCESSING,
    CAPTURED,
    FAILED,
    PARTIALLY_REFUNDED,
    REFUNDED,
    CANCELLED
}
