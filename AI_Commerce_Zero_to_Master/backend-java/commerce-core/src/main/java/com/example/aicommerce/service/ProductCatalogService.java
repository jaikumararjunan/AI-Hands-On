package com.example.aicommerce.service;

import com.example.aicommerce.model.Product;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class ProductCatalogService {
    private final Map<String, Product> products = new ConcurrentHashMap<>();

    public ProductCatalogService() {
        seed(new Product("P100", "AI Developer Laptop", "laptop", "NovaTech",
                "32GB RAM laptop for coding, local AI and productivity", new BigDecimal("129999"), 25));
        seed(new Product("P101", "Creator Laptop Pro", "laptop", "NovaTech",
                "High performance creator laptop with dedicated graphics", new BigDecimal("159999"), 14));
        seed(new Product("P200", "Noise Cancel Headphones", "audio", "Sonic",
                "Wireless over-ear headphones for travel and focus", new BigDecimal("12999"), 80));
        seed(new Product("P300", "4K USB-C Monitor", "monitor", "ViewMax",
                "27 inch 4K monitor with USB-C docking", new BigDecimal("34999"), 35));
        seed(new Product("P400", "Mechanical Keyboard", "accessory", "KeyForge",
                "Hot-swappable mechanical keyboard for developers", new BigDecimal("8999"), 100));
        seed(new Product("P500", "Laptop Dock", "accessory", "HubWorks",
                "USB-C dock with dual display, ethernet and charging", new BigDecimal("11999"), 60));
    }

    private void seed(Product product) {
        products.put(product.id(), product);
    }

    public List<Product> list() {
        return products.values().stream().toList();
    }

    public Product get(String id) {
        Product product = products.get(id);
        if (product == null) {
            throw new IllegalArgumentException("Unknown product: " + id);
        }
        return product;
    }
}
