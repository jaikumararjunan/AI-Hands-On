# Environment Promotion Model

One codebase, immutable build artifact, environment-specific configuration.

`development -> qa -> uat -> preprod -> production`

Do not compile different application logic for each stage. Promote the same tested artifact and inject configuration/secrets at deploy time.
