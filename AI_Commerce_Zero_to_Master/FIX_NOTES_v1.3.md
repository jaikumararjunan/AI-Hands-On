# v1.3 Fix Notes — Java RestClient Startup

## Symptom fixed

Spring Boot started Tomcat, then failed while creating `AiServiceClient`:

```text
No qualifying bean of type 'org.springframework.web.client.RestClient$Builder' available
```

## Root cause

`AiServiceClient` asks Spring to inject `RestClient.Builder`, but the project did not explicitly register that builder. In this Spring Boot 4 application, the current dependency set did not provide one automatically.

## Permanent fix

Added:

`backend-java/commerce-core/src/main/java/com/example/aicommerce/config/HttpClientConfig.java`

```java
@Configuration(proxyBeanMethods = false)
public class HttpClientConfig {
    @Bean
    RestClient.Builder restClientBuilder() {
        return RestClient.builder();
    }
}
```

`AiServiceClient` can keep constructor injection. This makes the outbound HTTP dependency explicit and testable.

## Regression protection

Added:

`backend-java/commerce-core/src/test/java/com/example/aicommerce/client/AiServiceClientContextTest.java`

The test boots a small Spring context and verifies that both `RestClient.Builder` and `AiServiceClient` are created.

## Docker diagnostics improvement

If `docker compose up` fails, the launcher now prints both Python and Java logs before exiting.

## Additional prevention

The Java Docker build now runs `mvn package` (including tests) instead of packaging with tests skipped. The runtime image also uses the real `/actuator/health` endpoint for its Docker health check instead of checking only `java -version`.

This means the container build/start sequence now catches more failures before the learner reaches the browser.
