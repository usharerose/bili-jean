# bili-jean

![license](https://img.shields.io/github/license/usharerose/bili-jean)
![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/usharerose/0390f119ad35dffc6e1e8441157d6f0f/raw/bili_jean_cov_badge.json)

Download Bilibili resources

## Development

### Environment

#### Docker (Recommended)
Execute the following commands, which sets up a service with development dependencies and enter into it.
```shell
> make run && make ssh
```

#### Virtual Environment
1. As a precondition, please [install Poetry](https://python-poetry.org/docs/1.7/#installation) which is a tool for dependency management and packaging in Python.
2. Install and activate local virtual environment
    ```shell
    > poetry install && poetry shell
    ```
3. `IPython` is provided as interactive shell

### Test

#### Docker Environment

* static check (code style)
  ```shell
  > make lintd
  ```

* static check (type hint)
  ```shell
  > make type-hintd
  ```

* unit test
  ```shell
  > make testd
  ```


#### Virtual Environment

* static check (code style)
  ```shell
  > make lint
  ```

* static check (type hint)
  ```shell
  > make type-hint
  ```

* unit test
  ```shell
  > make test
  ```
