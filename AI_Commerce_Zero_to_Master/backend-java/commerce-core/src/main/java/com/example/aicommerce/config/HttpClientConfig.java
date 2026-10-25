package com.example.aicommerce.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestClient;

/**
 * HTTP client factory shared by outbound REST integrations.
 *
 * Spring Boot 4 does not guarantee that a RestClient.Builder bean exists just
 * because spring-boot-starter-web is on the classpath. Providing the builder
 * explicitly keeps AiServiceClient startup deterministic in local Docker and
 * makes the dependency visible to learners.
 */
@Configuration(proxyBeanMethods = false)
public class HttpClientConfig {

    @Bean
    RestClient.Builder restClientBuilder() {
        return RestClient.builder();
    }
}
