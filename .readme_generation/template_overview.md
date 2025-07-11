# Microservice Repository Template

This is a template for GitHub repositories containing one Python-based microservice (optimal for a multirepository setup).

It features:

- *Continuous Templation* - A continuous update-delivery mechanism for templated repositories
- A [devcontainer](https://containers.dev/)-based fully-configured development environment for vscode
- Tight linting and formatting using [Ruff](https://docs.astral.sh/ruff/)
- Static type checking using [mypy](https://www.mypy-lang.org/)
- Security scanning using [bandit](https://bandit.readthedocs.io/en/latest/)
- A structure for automated tests using [pytest](https://docs.pytest.org/en/7.4.x/)
- Dependency locking using [pip-tools](https://github.com/jazzband/pip-tools)
- Git hooks checking linting and formatting before committing using [pre-commit](https://pre-commit.com/)
- Automatic container-building and publishing to [Docker Hub](https://hub.docker.com/)
- GitHub Actions for automating or checking all of the above

It is worth emphasizing the first point, this template is not just a one-time kickstart for your project
but repositories created using this template will continue receiving updates as the template evolves.
For further details, please look at the explanation in [.template/README.md](/.template/README.md).

Please also refer to [.readme_generation/README.md](/.readme_generation/README.md) for details on how
to adapt this readme.

Here the intro to the template stops and the actual template for the readme of the microservice starts:

---
