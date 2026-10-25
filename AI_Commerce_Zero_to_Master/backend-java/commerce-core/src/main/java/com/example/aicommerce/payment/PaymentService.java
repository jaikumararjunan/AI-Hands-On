package com.example.aicommerce.payment;

import com.example.aicommerce.model.PaymentIntentRequest;
import com.example.aicommerce.model.PaymentWebhookEvent;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class PaymentService {
    private final PaymentGateway gateway;
    private final Map<String, PaymentIntent> payments = new ConcurrentHashMap<>();
    private final Map<String, String> idempotencyIndex = new ConcurrentHashMap<>();
    private final Map<String, Boolean> processedWebhookEvents = new ConcurrentHashMap<>();

    public PaymentService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    /**
     * Idempotency prevents a network retry from creating a second payment intent.
     */
    public synchronized PaymentIntent createIntent(PaymentIntentRequest request, String idempotencyKey) {
        String existingPaymentId = idempotencyIndex.get(idempotencyKey);
        if (existingPaymentId != null) {
            return get(existingPaymentId);
        }

        GatewayResult result = gateway.create(request.orderId(), request.amount(), request.currency(),
                request.paymentMethodRef(), idempotencyKey);
        Instant now = Instant.now();
        String paymentId = "PAY-" + UUID.randomUUID();
        PaymentIntent payment = new PaymentIntent(
                paymentId,
                request.orderId(),
                request.amount(),
                request.currency().toUpperCase(),
                request.paymentMethodRef(),
                result.gatewayReference(),
                result.status(),
                BigDecimal.ZERO,
                result.nextAction(),
                now,
                now
        );
        payments.put(paymentId, payment);
        idempotencyIndex.putIfAbsent(idempotencyKey, paymentId);
        return payment;
    }

    public PaymentIntent confirm(String paymentId) {
        PaymentIntent current = get(paymentId);
        GatewayResult result = gateway.confirm(current.gatewayReference());
        return updateStatus(current, result.status(), current.refundedAmount(), result.nextAction());
    }

    public PaymentIntent capture(String paymentId) {
        PaymentIntent current = get(paymentId);
        GatewayResult result = gateway.capture(current.gatewayReference(), current.amount());
        return updateStatus(current, result.status(), current.refundedAmount(), result.nextAction());
    }

    public PaymentIntent refund(String paymentId, BigDecimal amount) {
        PaymentIntent current = get(paymentId);
        BigDecimal newRefunded = current.refundedAmount().add(amount);
        if (newRefunded.compareTo(current.amount()) > 0) {
            throw new IllegalArgumentException("Refund cannot exceed captured amount");
        }
        gateway.refund(current.gatewayReference(), amount);
        PaymentStatus status = newRefunded.compareTo(current.amount()) == 0
                ? PaymentStatus.REFUNDED : PaymentStatus.PARTIALLY_REFUNDED;
        return updateStatus(current, status, newRefunded, null);
    }

    /**
     * Mock webhook handler. A real provider adapter must verify the provider signature
     * before translating the event into this domain event.
     */
    public PaymentIntent handleWebhook(PaymentWebhookEvent event) {
        if (processedWebhookEvents.putIfAbsent(event.eventId(), true) != null) {
            return findByGatewayReference(event.gatewayReference());
        }
        PaymentIntent current = findByGatewayReference(event.gatewayReference());
        PaymentStatus target = switch (event.eventType()) {
            case "payment.succeeded" -> PaymentStatus.CAPTURED;
            case "payment.processing" -> PaymentStatus.PROCESSING;
            case "payment.failed" -> PaymentStatus.FAILED;
            case "payment.cancelled" -> PaymentStatus.CANCELLED;
            default -> current.status();
        };
        return updateStatus(current, target, current.refundedAmount(), null);
    }

    public PaymentIntent get(String paymentId) {
        PaymentIntent payment = payments.get(paymentId);
        if (payment == null) {
            throw new IllegalArgumentException("Unknown payment: " + paymentId);
        }
        return payment;
    }

    private PaymentIntent findByGatewayReference(String gatewayReference) {
        return payments.values().stream()
                .filter(p -> p.gatewayReference().equals(gatewayReference))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("Unknown gateway reference: " + gatewayReference));
    }

    private PaymentIntent updateStatus(PaymentIntent current, PaymentStatus status,
                                       BigDecimal refundedAmount, String nextAction) {
        PaymentIntent updated = new PaymentIntent(
                current.paymentId(), current.orderId(), current.amount(), current.currency(),
                current.paymentMethodRef(), current.gatewayReference(), status, refundedAmount,
                nextAction, current.createdAt(), Instant.now());
        payments.put(current.paymentId(), updated);
        return updated;
    }
}
