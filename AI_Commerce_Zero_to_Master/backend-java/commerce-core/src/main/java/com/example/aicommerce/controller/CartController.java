package com.example.aicommerce.controller;

import com.example.aicommerce.model.Cart;
import com.example.aicommerce.model.CartItem;
import com.example.aicommerce.service.CartService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/carts")
public class CartController {
    private final CartService carts;

    public CartController(CartService carts) {
        this.carts = carts;
    }

    @GetMapping("/{customerId}")
    public Cart get(@PathVariable String customerId) {
        return carts.get(customerId);
    }

    @PostMapping("/{customerId}/items")
    public Cart add(@PathVariable String customerId, @RequestBody CartItem item) {
        return carts.add(customerId, item);
    }

    @DeleteMapping("/{customerId}")
    public void clear(@PathVariable String customerId) {
        carts.clear(customerId);
    }
}
