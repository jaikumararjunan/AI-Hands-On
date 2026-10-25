package com.example.aicommerce.event;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

@Component
@Profile("!kafka")
public class LoggingOrderEventPublisher implements OrderEventPublisher {
    private static final Logger log = LoggerFactory.getLogger(LoggingOrderEventPublisher.class);

    @Override
    public void publish(OrderCreatedEvent event) {
        log.info("ORDER_CREATED {}", event);
    }
}
