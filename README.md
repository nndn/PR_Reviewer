# PR Reviewer Agent: Automatic reviews for PRs by AI

Try it out:

- once server is up, you can use /docs to get oapi ui, use it to playaround
- ex: http://127.0.0.1:8080/docs -> local default development

# setup

Dependencies:

- postgres (docker-compose) -> alembic migrations
- redis (docker-compose)
- openai / openrouter api key
- github access key
- pip install requirements.txt

# development

Architecture:

- uses (hexagonal architecture)[https://alistair.cockburn.us/hexagonal-architecture/] pattern

  - code is split into layers
  - domain layer: contains core definitions of domain entities (pr, review, task structs)
  - application layer: application logic + monitoring + logging etc
  - adapters: all the external dependencies (databases, external api calls, http servers etd)
    - adapters can be outbound or inbound
  - ports: adapter and application layer don't talk directly, they implement ports
  - we get modular, extensible and testable entities

  - for smaller projects we can get rid of few abstractions to simplify code:

    - can move outbound port to main file
    - merge domain, ports and application into single module
    - application and adapters need to be seperate as we need dependecy inversion there

  - for larger projects we can stream line more:

    - break down application logic into commands and queries
    - this helps reuse common commands and also helps implement CQRS

- pr_reviewer/server.py is main entry point to the server

  - server runs a fastapi http server aswell as a celery job queue in seperate threads
  - celery task is registered in main and passed to the crud server
  - crud server invokes celery task on request

TODO: current:

- implement exhaustive error handling. Especially for external rate-limits etc
- use structured logger that is defined, figure out what to do with celery, fastapi logs
- fine tune and improve prompts in reviewer application, start batching inference

TODO: new features:

- register a repository for context rich review (create a new reviewer application)
- access some kind of heirarchical RAG / pre computed data to get context the code
- github bot and webhook server that automatically reviews on pr creation
- deliver email/slack/ms-teams notifications when review done
