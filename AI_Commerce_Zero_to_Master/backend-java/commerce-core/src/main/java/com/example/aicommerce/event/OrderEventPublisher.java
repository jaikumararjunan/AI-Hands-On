package com.example.aicommerce.event;

public interface OrderEventPublisher {
    void publish(OrderCreatedEvent event);
}
