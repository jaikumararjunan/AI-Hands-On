package com.example.aicommerce.client;

import com.example.aicommerce.config.HttpClientConfig;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.web.client.RestClient;

import static org.assertj.core.api.Assertions.assertThat;

class AiServiceClientContextTest {

    private final ApplicationContextRunner contextRunner = new ApplicationContextRunner()
            .withUserConfiguration(TestConfig.class)
            .withPropertyValues("app.ai.base-url=http://localhost:8000");

    @Test
    void createsRestClientBuilderAndAiServiceClient() {
        contextRunner.run(context -> {
            assertThat(context).hasSingleBean(RestClient.Builder.class);
            assertThat(context).hasSingleBean(AiServiceClient.class);
        });
    }

    @Configuration(proxyBeanMethods = false)
    @Import({HttpClientConfig.class, AiServiceClient.class})
    static class TestConfig {
    }
}
