package com.example.aicommerce.controller;

import com.example.aicommerce.model.CheckoutRequest;
import com.example.aicommerce.model.CheckoutResponse;
import com.example.aicommerce.service.CheckoutService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/checkout")
public class CheckoutController {
    private final CheckoutService checkout;

    public CheckoutController(CheckoutService checkout) {
        this.checkout = checkout;
    }

    @PostMapping
    public CheckoutResponse checkout(@Valid @RequestBody CheckoutRequest request,
                                     @RequestHeader("Idempotency-Key") String idempotencyKey) {
        return checkout.checkout(request, idempotencyKey);
    }
}
