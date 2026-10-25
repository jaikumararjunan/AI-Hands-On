package com.example.aicommerce.model;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

import java.math.BigDecimal;

public record PaymentIntentRequest(
        @NotBlank String orderId,
        @NotNull @Positive BigDecimal amount,
        @NotBlank String currency,
        @NotBlank String paymentMethodRef
) {}
