package com.example.aicommerce.controller;

import com.example.aicommerce.client.AiServiceClient;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/ai")
public class AiInsightsController {
    private final AiServiceClient ai;

    public AiInsightsController(AiServiceClient ai) {
        this.ai = ai;
    }

    @GetMapping("/search")
    public Map<String, Object> search(@RequestParam String q) {
        return ai.semanticSearch(q);
    }

    @GetMapping("/recommendations/{customerId}")
    public Map<String, Object> recommendations(@PathVariable String customerId) {
        return ai.recommendations(customerId);
    }

    @PostMapping("/ask")
    public Map<String, Object> ask(@RequestBody Map<String, String> body) {
        return ai.askAgent(body.getOrDefault("question", ""));
    }
}
