$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\backend-java\commerce-core"
mvn spring-boot:run
