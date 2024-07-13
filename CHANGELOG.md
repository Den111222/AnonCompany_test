Для корректной работы и чтобы удовлетворять всем правилам `wemake-python-styleguide`
внес корректировку в `flake8.toml`:

*строку*

``per-file-ignores = "tests/**.py: S101, S106, D103, ANN201, WPS442"``

*заменил на строку*

``per-file-ignores = "app/tests/**.py: S101, S106, D103, ANN201, WPS442"``
