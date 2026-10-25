package com.example.aicommerce.payment;

import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Safe local gateway simulator. It never accepts PAN/CVV or real bank credentials.
 * Special token refs are useful for deterministic learning:
 * pm_auth_* -> requires additional authentication; pm_fail_* -> failed.
 */
@Component
public class MockPaymentGateway implements PaymentGateway {
    private final Map<String, GatewayResult> states = new ConcurrentHashMap<>();
    private final Map<String, String> idempotency = new ConcurrentHashMap<>();

    @Override
    public synchronized GatewayResult create(String orderId, BigDecimal amount, String currency,
                                             String paymentMethodRef, String idempotencyKey) {
        String existingReference = idempotency.get(idempotencyKey);
        if (existingReference != null) {
            return states.get(existingReference);
        }
        String reference = "MOCK-GW-" + UUID.randomUUID();
        GatewayResult result;
        if (paymentMethodRef.startsWith("pm_fail")) {
            result = new GatewayResult(reference, PaymentStatus.FAILED, null);
        } else if (paymentMethodRef.startsWith("pm_auth")) {
            result = new GatewayResult(reference, PaymentStatus.REQUIRES_ACTION, "mock://3ds/" + reference);
        } else {
            result = new GatewayResult(reference, PaymentStatus.AUTHORIZED, null);
        }
        idempotency.put(idempotencyKey, reference);
        states.put(reference, result);
        return result;
    }

    @Override
    public GatewayResult confirm(String gatewayReference) {
        GatewayResult current = get(gatewayReference);
        GatewayResult result = current.status() == PaymentStatus.REQUIRES_ACTION
                ? new GatewayResult(gatewayReference, PaymentStatus.AUTHORIZED, null)
                : current;
        states.put(gatewayReference, result);
        return result;
    }

    @Override
    public GatewayResult capture(String gatewayReference, BigDecimal amount) {
        GatewayResult current = get(gatewayReference);
        if (current.status() != PaymentStatus.AUTHORIZED && current.status() != PaymentStatus.PROCESSING) {
            return current;
        }
        GatewayResult result = new GatewayResult(gatewayReference, PaymentStatus.CAPTURED, null);
        states.put(gatewayReference, result);
        return result;
    }

    @Override
    public GatewayResult refund(String gatewayReference, BigDecimal amount) {
        get(gatewayReference);
        GatewayResult result = new GatewayResult(gatewayReference, PaymentStatus.REFUNDED, null);
        states.put(gatewayReference, result);
        return result;
    }

    private GatewayResult get(String gatewayReference) {
        GatewayResult result = states.get(gatewayReference);
        if (result == null) {
            throw new IllegalArgumentException("Unknown gateway reference: " + gatewayReference);
        }
        return result;
    }
}
