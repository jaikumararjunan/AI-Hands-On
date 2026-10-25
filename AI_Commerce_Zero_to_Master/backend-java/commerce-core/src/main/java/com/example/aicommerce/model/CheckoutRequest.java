package com.example.aicommerce.model;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record CheckoutRequest(
        @NotNull @Valid OrderRequest order,
        @NotBlank String currency,
        @NotBlank String paymentMethodRef
) {}
