package com.example.aicommerce.service;

import com.example.aicommerce.model.Cart;
import com.example.aicommerce.model.CartItem;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class CartService {
    private final Map<String, List<CartItem>> carts = new ConcurrentHashMap<>();

    public Cart get(String customerId) {
        return new Cart(customerId, List.copyOf(carts.getOrDefault(customerId, List.of())));
    }

    public Cart add(String customerId, CartItem item) {
        carts.compute(customerId, (key, current) -> {
            List<CartItem> next = current == null ? new ArrayList<>() : new ArrayList<>(current);
            next.add(item);
            return next;
        });
        return get(customerId);
    }

    public void clear(String customerId) {
        carts.remove(customerId);
    }
}
