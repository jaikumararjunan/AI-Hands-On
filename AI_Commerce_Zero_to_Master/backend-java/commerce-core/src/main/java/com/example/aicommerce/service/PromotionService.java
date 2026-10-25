package com.example.aicommerce.service;

import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Legacy-style deterministic promotion rules.
 * Keep regulated/contractual business rules deterministic even when AI recommendations exist.
 */
@Service
public class PromotionService {
    public BigDecimal calculateDiscount(String couponCode, BigDecimal subtotal) {
        if (couponCode == null || couponCode.isBlank()) {
            return BigDecimal.ZERO;
        }
        return switch (couponCode.toUpperCase()) {
            case "WELCOME10" -> subtotal.multiply(new BigDecimal("0.10")).setScale(2, RoundingMode.HALF_UP);
            case "FESTIVE5" -> subtotal.multiply(new BigDecimal("0.05")).setScale(2, RoundingMode.HALF_UP);
            default -> BigDecimal.ZERO;
        };
    }
}
