# Slack slash command receiver

**A tiny microservice to receive slash command requests from Slack.**


The service mainly does three things:
* It transforms the request from `application/x-www-form-urlencoded` to `application/json`.
* It generates a uuid to give each request a unique id before it's forwarded to a http_endpoint pipe.
* It validates the verification token defined in the Slack app. 

### Example config

```json
{
  "_id": "slack-command-receiver",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "ENDPOINT_URL": "$ENV(slack-command-pipe-endpoint)",
      "LOG_LEVEL": "INFO",
      "NODE_JWT": "$SECRET(slack-command-jwt)",
      "VALIDATION_TOKEN": "$SECRET(slack-command-validation-token)"
    },
    "image": "sesamcommunity/slack-slash-command-receiver",
    "port": 5000
  },
  "verify_ssl": true
}
```

### Variables

* ENDPOINT_URL     - The full url for the http_endpoint pipe (i.e. https://datahub-XXXXXX.sesam.cloud/api/receivers/slack-command/entities)
* LOG_LEVEL        - Optional, Default is INFO
* NODE_JWT         - JWT to get write access to endpoint pipe
* VALIDATION_TOKEN - Slack app verification token

