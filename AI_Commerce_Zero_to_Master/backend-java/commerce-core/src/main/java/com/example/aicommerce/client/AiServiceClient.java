package com.example.aicommerce.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

import java.util.Map;

@Component
public class AiServiceClient {
    private final RestClient client;

    public AiServiceClient(RestClient.Builder builder,
                           @Value("${app.ai.base-url:http://localhost:8000}") String baseUrl) {
        this.client = builder.baseUrl(baseUrl).build();
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> semanticSearch(String query) {
        return client.get()
                .uri(uri -> uri.path("/ai/search").queryParam("q", query).build())
                .retrieve()
                .body(Map.class);
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> askAgent(String question) {
        return client.post()
                .uri("/ai/agent/ask")
                .body(Map.of("question", question))
                .retrieve()
                .body(Map.class);
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> recommendations(String customerId) {
        return client.get()
                .uri("/ai/recommendations/{customerId}", customerId)
                .retrieve()
                .body(Map.class);
    }
}
