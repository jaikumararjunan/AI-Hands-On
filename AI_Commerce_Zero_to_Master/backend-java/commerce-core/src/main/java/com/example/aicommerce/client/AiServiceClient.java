package com.example.aicommerce.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestClientResponseException;

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
                .accept(MediaType.APPLICATION_JSON)
                .retrieve()
                .body(Map.class);
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> askAgent(String question) {
        try {
            String payload = "{\"question\":" + jsonString(question == null ? "" : question) + "}";
            Map<String, Object> response = client.post()
                    .uri("/ai/agent/ask")
                    .contentType(MediaType.APPLICATION_JSON)
                    .accept(MediaType.APPLICATION_JSON)
                    .body(payload)
                    .retrieve()
                    .body(Map.class);

            return response == null
                    ? Map.of(
                            "route", "error",
                            "answer", "The Python AI service returned an empty response.",
                            "degraded", true)
                    : response;
        } catch (RestClientResponseException error) {
            String responseBody = error.getResponseBodyAsString();
            return Map.of(
                    "route", "error",
                    "answer", "The Python AI service returned HTTP " + error.getStatusCode().value()
                            + ". Check ai-python logs for the detailed cause.",
                    "degraded", true,
                    "downstreamStatus", error.getStatusCode().value(),
                    "diagnostic", error.getClass().getSimpleName(),
                    "downstreamBody", responseBody == null ? "" : responseBody);
        } catch (RestClientException error) {
            return Map.of(
                    "route", "error",
                    "answer", "The Java commerce service could not reach the Python AI service.",
                    "degraded", true,
                    "diagnostic", error.getClass().getSimpleName());
        }
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> recommendations(String customerId) {
        return client.get()
                .uri("/ai/recommendations/{customerId}", customerId)
                .accept(MediaType.APPLICATION_JSON)
                .retrieve()
                .body(Map.class);
    }

    private static String jsonString(String value) {
        StringBuilder result = new StringBuilder(value.length() + 2).append('"');
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            switch (c) {
                case '"' -> result.append("\\\"");
                case '\\' -> result.append("\\\\");
                case '\b' -> result.append("\\b");
                case '\f' -> result.append("\\f");
                case '\n' -> result.append("\\n");
                case '\r' -> result.append("\\r");
                case '\t' -> result.append("\\t");
                default -> {
                    if (c < 0x20) {
                        result.append(String.format("\\u%04x", (int) c));
                    } else {
                        result.append(c);
                    }
                }
            }
        }
        return result.append('"').toString();
    }
}
