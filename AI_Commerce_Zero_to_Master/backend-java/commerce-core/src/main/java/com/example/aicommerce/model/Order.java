package com.example.aicommerce.model;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

public record Order(
        String orderId,
        String customerId,
        List<CartItem> items,
        BigDecimal subtotal,
        BigDecimal discount,
        BigDecimal total,
        String status,
        Instant createdAt
) {}
