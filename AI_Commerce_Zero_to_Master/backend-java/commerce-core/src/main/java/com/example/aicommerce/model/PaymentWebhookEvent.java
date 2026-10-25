package com.example.aicommerce.model;

import jakarta.validation.constraints.NotBlank;

public record PaymentWebhookEvent(
        @NotBlank String eventId,
        @NotBlank String eventType,
        @NotBlank String gatewayReference
) {}
