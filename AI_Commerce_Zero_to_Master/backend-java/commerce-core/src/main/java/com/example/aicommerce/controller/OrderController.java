package com.example.aicommerce.controller;

import com.example.aicommerce.model.Order;
import com.example.aicommerce.model.OrderRequest;
import com.example.aicommerce.service.OrderService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderService orders;

    public OrderController(OrderService orders) {
        this.orders = orders;
    }

    @PostMapping
    public Order create(@Valid @RequestBody OrderRequest request) {
        return orders.create(request);
    }

    @GetMapping("/{orderId}")
    public Order get(@PathVariable String orderId) {
        return orders.get(orderId);
    }
}
