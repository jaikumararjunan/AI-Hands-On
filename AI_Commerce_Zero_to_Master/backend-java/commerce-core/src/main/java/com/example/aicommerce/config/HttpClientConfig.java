package com.example.aicommerce.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestClient;

import java.time.Duration;

/**
 * HTTP client factory shared by outbound REST integrations.
 *
 * The AI service is Uvicorn/FastAPI over plain HTTP inside Docker. The default
 * JDK-backed client can attempt an h2c (HTTP/2 clear-text) upgrade; Uvicorn does
 * not support that upgrade and POST request bodies can be lost during fallback.
 * Using Spring's SimpleClientHttpRequestFactory keeps this internal service call
 * on HTTP/1.1 and makes Java -> Python POST requests deterministic.
 */
@Configuration(proxyBeanMethods = false)
public class HttpClientConfig {

    @Bean
    RestClient.Builder restClientBuilder() {
        SimpleClientHttpRequestFactory requestFactory = new SimpleClientHttpRequestFactory();
        requestFactory.setConnectTimeout(Duration.ofSeconds(5));
        requestFactory.setReadTimeout(Duration.ofSeconds(45));

        return RestClient.builder()
                .requestFactory(requestFactory);
    }
}
