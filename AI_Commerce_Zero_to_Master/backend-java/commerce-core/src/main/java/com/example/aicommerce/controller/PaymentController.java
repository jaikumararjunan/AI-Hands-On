package com.example.aicommerce.controller;

import com.example.aicommerce.model.PaymentIntentRequest;
import com.example.aicommerce.model.PaymentWebhookEvent;
import com.example.aicommerce.model.RefundRequest;
import com.example.aicommerce.payment.PaymentIntent;
import com.example.aicommerce.payment.PaymentService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/payments")
public class PaymentController {
    private final PaymentService payments;

    public PaymentController(PaymentService payments) {
        this.payments = payments;
    }

    @PostMapping("/intents")
    public PaymentIntent create(@Valid @RequestBody PaymentIntentRequest request,
                                @RequestHeader(value = "Idempotency-Key", required = false) String idempotencyKey) {
        String key = idempotencyKey == null || idempotencyKey.isBlank()
                ? UUID.randomUUID().toString() : idempotencyKey;
        return payments.createIntent(request, key);
    }

    @PostMapping("/{paymentId}/confirm")
    public PaymentIntent confirm(@PathVariable String paymentId) {
        return payments.confirm(paymentId);
    }

    @PostMapping("/{paymentId}/capture")
    public PaymentIntent capture(@PathVariable String paymentId) {
        return payments.capture(paymentId);
    }

    @PostMapping("/{paymentId}/refunds")
    public PaymentIntent refund(@PathVariable String paymentId, @Valid @RequestBody RefundRequest request) {
        return payments.refund(paymentId, request.amount());
    }

    @GetMapping("/{paymentId}")
    public PaymentIntent get(@PathVariable String paymentId) {
        return payments.get(paymentId);
    }

    @PostMapping("/webhooks/mock")
    public ResponseEntity<PaymentIntent> mockWebhook(@Valid @RequestBody PaymentWebhookEvent event) {
        return ResponseEntity.ok(payments.handleWebhook(event));
    }
}
