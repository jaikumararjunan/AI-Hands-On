package com.example.aicommerce.mcp;

import com.example.aicommerce.model.Product;
import com.example.aicommerce.service.OrderService;
import com.example.aicommerce.service.ProductCatalogService;
import org.springframework.ai.mcp.annotation.McpTool;
import org.springframework.ai.mcp.annotation.McpToolParam;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * MCP makes existing deterministic commerce capabilities discoverable to AI hosts.
 * The tool layer delegates to the same domain services used by REST controllers.
 */
@Component
public class CommerceMcpTools {
    private final ProductCatalogService catalog;
    private final OrderService orders;

    public CommerceMcpTools(ProductCatalogService catalog, OrderService orders) {
        this.catalog = catalog;
        this.orders = orders;
    }

    @McpTool(
            name = "commerce_list_products",
            description = "List the current demo commerce catalog. Read-only.",
            annotations = @McpTool.McpAnnotations(
                    readOnlyHint = true,
                    destructiveHint = false,
                    idempotentHint = true,
                    openWorldHint = false
            )
    )
    public List<Product> listProducts() {
        return catalog.list();
    }

    @McpTool(
            name = "commerce_get_product",
            description = "Read one product by product id. Read-only.",
            annotations = @McpTool.McpAnnotations(
                    readOnlyHint = true,
                    destructiveHint = false,
                    idempotentHint = true,
                    openWorldHint = false
            )
    )
    public Product getProduct(
            @McpToolParam(description = "Product id such as P100", required = true) String productId) {
        return catalog.get(productId);
    }

    @McpTool(
            name = "commerce_get_order",
            description = "Read an existing order by id. Read-only.",
            annotations = @McpTool.McpAnnotations(
                    readOnlyHint = true,
                    destructiveHint = false,
                    idempotentHint = true,
                    openWorldHint = false
            )
    )
    public Object getOrder(
            @McpToolParam(description = "Order id returned by the order API", required = true) String orderId) {
        return orders.get(orderId);
    }
}
