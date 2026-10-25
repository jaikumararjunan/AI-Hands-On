package com.example.aicommerce.event;

import java.math.BigDecimal;
import java.time.Instant;

public record OrderCreatedEvent(
        String orderId,
        String customerId,
        BigDecimal total,
        Instant createdAt
) {}
