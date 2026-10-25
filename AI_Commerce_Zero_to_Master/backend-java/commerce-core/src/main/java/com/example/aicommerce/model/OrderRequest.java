package com.example.aicommerce.model;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import java.util.List;

public record OrderRequest(
        @NotBlank String customerId,
        @NotEmpty List<CartItem> items,
        String couponCode
) {}
