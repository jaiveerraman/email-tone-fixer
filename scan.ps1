# Runs tests with coverage, then runs a SonarQube analysis against the local
# server started by docker-compose.yml (http://localhost:9000).
#
# First-time setup:
#   1. docker compose up -d
#   2. Open http://localhost:9000 (default login admin/admin, you'll be asked to change it)
#   3. Create a local project with key "email-tone-fixer" and generate a token
#      (My Account > Security > Generate Token)
#   4. $env:SONAR_TOKEN = "<paste token>"
#
# Then run this script from the repo root whenever you want a fresh scan:
#   ./scan.ps1

if (-not $env:SONAR_TOKEN) {
    Write-Error "SONAR_TOKEN is not set. Generate a token in SonarQube (My Account > Security) and run: `$env:SONAR_TOKEN = '<token>'"
    exit 1
}

Write-Host "Running tests with coverage..."
uv run python -m pytest eval/ --cov=. --cov-report=xml
if ($LASTEXITCODE -ne 0) {
    Write-Error "Tests failed — fix them before scanning."
    exit 1
}

Write-Host "Running sonar-scanner..."
# host.docker.internal lets the scanner container reach the SonarQube
# container/port published on the host by docker-compose.yml.
docker run --rm `
    -e SONAR_HOST_URL="http://host.docker.internal:9000" `
    -e SONAR_TOKEN="$env:SONAR_TOKEN" `
    -v "${PWD}:/usr/src" `
    sonarsource/sonar-scanner-cli

Write-Host "Done. View results at http://localhost:9000/dashboard?id=email-tone-fixer"
