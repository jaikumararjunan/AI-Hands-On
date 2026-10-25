package com.example.aicommerce.model;

import java.util.List;

public record Cart(String customerId, List<CartItem> items) {}
