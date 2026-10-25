package com.example.aicommerce.model;

import java.math.BigDecimal;

public record Product(
        String id,
        String name,
        String category,
        String brand,
        String description,
        BigDecimal price,
        int inventory
) {}
