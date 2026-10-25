package com.example.aicommerce.controller;

import com.example.aicommerce.model.Product;
import com.example.aicommerce.service.ProductCatalogService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class CatalogController {
    private final ProductCatalogService catalog;

    public CatalogController(ProductCatalogService catalog) {
        this.catalog = catalog;
    }

    @GetMapping
    public List<Product> list() {
        return catalog.list();
    }

    @GetMapping("/{id}")
    public Product get(@PathVariable String id) {
        return catalog.get(id);
    }
}
