package com.example.aicommerce.service;

import com.example.aicommerce.event.OrderCreatedEvent;
import com.example.aicommerce.event.OrderEventPublisher;
import com.example.aicommerce.model.CartItem;
import com.example.aicommerce.model.Order;
import com.example.aicommerce.model.OrderRequest;
import com.example.aicommerce.model.Product;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class OrderService {
    private final ProductCatalogService catalog;
    private final PromotionService promotions;
    private final OrderEventPublisher publisher;
    private final Map<String, Order> orders = new ConcurrentHashMap<>();

    public OrderService(ProductCatalogService catalog, PromotionService promotions, OrderEventPublisher publisher) {
        this.catalog = catalog;
        this.promotions = promotions;
        this.publisher = publisher;
    }

    public Order create(OrderRequest request) {
        BigDecimal subtotal = BigDecimal.ZERO;
        for (CartItem item : request.items()) {
            Product product = catalog.get(item.productId());
            subtotal = subtotal.add(product.price().multiply(BigDecimal.valueOf(item.quantity())));
        }
        BigDecimal discount = promotions.calculateDiscount(request.couponCode(), subtotal);
        BigDecimal total = subtotal.subtract(discount);
        String orderId = "ORD-" + UUID.randomUUID();
        Instant now = Instant.now();
        Order order = new Order(orderId, request.customerId(), request.items(), subtotal, discount,
                total, "CREATED", now);
        orders.put(orderId, order);
        publisher.publish(new OrderCreatedEvent(orderId, request.customerId(), total, now));
        return order;
    }

    public Order get(String orderId) {
        Order order = orders.get(orderId);
        if (order == null) {
            throw new IllegalArgumentException("Unknown order: " + orderId);
        }
        return order;
    }
}
