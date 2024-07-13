# AnonCompany_test
Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий содержимое HEAD репозитория
https://gitea.radium.group/radium/project-configuration во временную папку.
После выполнения всех асинхронных задач скрипт должен посчитать sha256 хэши от каждого файла.
Код должен проходить без замечаний проверку линтером wemake-python-styleguide. Конфигурация
nitpick - https://gitea.radium.group/radium/project-configuration
Обязательно 100% покрытие тестами

* Прошу ответить на следующие вопросы:
* * Как вы реализовали асинхронное выполнение задач в вашем скрипте?
* * Какие библиотеки использовались для скачивания содержимого репозитория и для каких целей?
* * Какие проблемы асинхронности вы сталкивались при выполнении задания и как их решали?
* * Как вы организовали скачивание файлов во временную папку?
* * Какие основные требования wemake-python-styleguide вы находите наиболее важными для поддержания качества кода?
* * Как вы настраивали свой проект для соответствия конфигурации nitpick, указанной в задании? Были ли трудности при настройке?
* * Какие инструменты использовали для измерения 100% покрытия тестами?
* * Какие типы тестов вы написали для проверки функциональности вашего скрипта? (Например, модульные тесты, интеграционные тесты)
* * Как вы тестировали асинхронный код? Использовали ли вы моки (mocks) или стабы (stubs) для тестирования асинхронныx операций?

# Ответы:
1. Как вы реализовали асинхронное выполнение задач в вашем скрипте?:
* * Асинхронное выполнение задач в скрипте реализовано с помощью библиотеки `asyncio`, которая позволяет выполнять задачи параллельно, не блокируя основной поток выполнения. Основные функции, такие как `fetch_file_list`, `download_files`, `process_files` и `main`, были определены как `async` функции, чтобы они могли выполняться асинхронно.
2. Какие библиотеки использовались для скачивания содержимого репозитория и для каких целей?
* * Для скачивания содержимого репозитория использовались следующие библиотеки:

* * * `aiohttp`: Используется для выполнения асинхронных HTTP-запросов. С её помощью загружаются списки файлов и содержимое файлов из репозитория.
* * * `aioresponses`: Используется для мока HTTP-запросов в тестах, чтобы симулировать ответы сервера и проверить работу асинхронного кода.
3. Какие проблемы асинхронности вы сталкивались при выполнении задания и как их решали?
* * Основные проблемы асинхронности включают:
* * * Конкурентный доступ к ресурсам: Необходимо было обеспечить, чтобы различные асинхронные задачи корректно работали с общими ресурсами, такими как временные файлы.
* * * Синхронизация задач: Убедиться, что все задачи завершены корректно до завершения основной функции.
* * * Тестирование асинхронного кода: Асинхронный код требует специальных методов тестирования, таких как использование `aioresponses` и `AsyncMock`.
* * Эти проблемы решались использованием подходящих библиотек и инструментов для управления асинхронными задачами и тестирования.
4. Как вы организовали скачивание файлов во временную папку?
* * Скачивание файлов во временную папку организовано с использованием библиотеки `pathlib` для работы с путями файловой системы. Файлы скачиваются во временную директорию, предоставленную `pytest` через параметр `tmp_path`. Для каждого файла создается полный путь, и содержимое файла записывается в соответствующий путь с использованием метода `write_bytes`.
5. Какие основные требования `wemake-python-styleguide` вы находите наиболее важными для поддержания качества кода?
* Чистота и читаемость кода
* * Максимальная длина строки: Код должен быть не более 79 символов в строке. Это помогает избежать горизонтальной прокрутки и улучшает читаемость кода.
* * Разделение функций и методов: Одна функция или метод должна выполнять одну задачу. Это делает код более модульным и легко тестируемым.
* * Именование переменных и функций: Имена должны быть понятными и описательными. Например, `calculate_sha256` вместо `calc_sha`.
* Минимизация сложности
* * Ограничение количества локальных переменных: Максимум 5 локальных переменных на функцию. Это снижает сложность функции и упрощает понимание кода.
    Хотя ограничение на количество локальных переменных помогает уменьшить сложность функции и улучшить её тестируемость, оно может привести к другим проблемам, таким как усложнение логики, повышение когнитивной нагрузки и избыточная абстракция. Важно соблюдать баланс и применять это правило осмысленно, учитывая контекст и специфику задачи.
* * Ограничение вложенности: Максимальная вложенность не должна превышать 4 уровня. Это предотвращает создание сложных и запутанных структур.
* Явные конструкции и отсутствие магии
* * Запрет магических чисел и строк: Все числа и строки, используемые в коде, должны быть объявлены как константы. Это помогает избежать непредвиденных ошибок и улучшает понимание кода.
* * Явные возвращаемые значения: Функции должны явно возвращать значения, чтобы было понятно, что они делают.
* Согласованность и стандарты оформления
* * Докстринги: Все модули, классы и функции должны иметь докстринги. Это улучшает документацию и помогает другим разработчикам понять назначение и использование кода.
* * Организация импорта: Импорты должны быть упорядочены и разделены на три группы: стандартные библиотеки, сторонние библиотеки и локальные модули.
* Безопасность и производительность
* * Запрет использования assert для проверки: В продакшн коде assert может быть отключен, поэтому вместо него следует использовать явные проверки и исключения.
* * Запрет использования eval и exec: Эти функции могут быть опасными и привести к уязвимостям в безопасности.
* Тестируемость
* * Максимальное покрытие тестами: Код должен быть покрыт тестами как можно полнее. Это включает как модульные тесты, так и интеграционные тесты.
* * Чистота тестов: Тесты должны быть простыми и понятными. Следует избегать сложной логики в тестах.
6. Как вы настраивали свой проект для соответствия конфигурации `nitpick`, указанной в задании? Были ли трудности при настройке?
* * Проект настраивался для соответствия конфигурации `nitpick` путем создания и настройки файлов конфигурации, таких как `setup.cfg` и `.editorconfig`. Основные трудности включали необходимость точной настройки стиля кода, чтобы удовлетворять всем правилам `wemake-python-styleguide`, а также интеграция этих инструментов в процесс разработки.
7. Какие инструменты использовали для измерения 100% покрытия тестами?
* * Для измерения покрытия тестами использовались следующие инструменты:
* * * `pytest-cov`: Плагин для `pytest`, который измеряет покрытие кода тестами.
* * * `coverage.py`: Библиотека, используемая `pytest-cov` для детального отчета о покрытии.
8. Какие типы тестов вы написали для проверки функциональности вашего скрипта? (Например, модульные тесты, интеграционные тесты)
* * Модульные тесты. Этот тип тестов проверяет работу отдельных функций и методов в изоляции от других частей системы. Для скрипта были созданы тесты для следующих функций:
* * * `fetch_file_list`: проверка, что функция корректно возвращает список файлов из ответа API.
* * * `download_files`: проверка, что функция корректно скачивает файлы и сохраняет их во временную директорию.
* * * `process_files`: проверка, что функция корректно вычисляет SHA-256 хэш содержимого файлов.
* * * `calculate_sha256`: проверка, что функция корректно вычисляет SHA-256 хэш содержимого одного файла.
* * * `split_list`: проверка, что функция корректно делит список файлов на чанки заданного размера.
* * Интеграционные тесты. Эти тесты проверяют взаимодействие между различными частями системы. Они проверяют, что функции корректно работают вместе и обрабатывают данные на всех этапах выполнения скрипта. Для скрипта были созданы тесты для следующих сценариев:
* * * Полный сценарий выполнения основного процесса в функции main, включая получение списка файлов, скачивание файлов, вычисление хэшей и проверку корректности выполнения всех задач.
* * Функциональные тесты. Эти тесты проверяют основные сценарии использования и функциональность системы с точки зрения конечного пользователя. Эти тесты проверяют, что система выполняет свои основные функции корректно и полностью. В контексте скрипта функциональные тесты были сфокусированы на:
* * * Проверке, что скрипт корректно скачивает указанные файлы и сохраняет их в целевую директорию.
* * * Проверке, что скрипт корректно вычисляет и возвращает ожидаемые хэши для скачанных файлов.
* * Асинхронные тесты. Эти тесты проверяют асинхронные функции и методы, чтобы убедиться, что они корректно выполняются и обрабатывают асинхронные задачи. В данном проекте такие тесты включают:
* * * Проверку асинхронных функций `fetch_file_list`, `download_files`, `process_files`, чтобы убедиться, что они корректно работают с асинхронными HTTP-запросами и файлами.
9. Как вы тестировали асинхронный код? Использовали ли вы моки (`mocks`) или стабы (`stubs`) для тестирования асинхронныx операций?
* * Асинхронный код тестировался с использованием библиотеки `aioresponses` для мока HTTP-запросов и ответа от сервера. Кроме того, использовался `AsyncMock` из библиотеки `unittest.mock` для мока асинхронных функций и методов. Это позволило эффективно симулировать различные сценарии и проверить корректность работы асинхронного кода.


# AnonCompany_test

## Description

Write a script that asynchronously performs 3 concurrent tasks to download the contents of the HEAD of the repository at [https://gitea.radium.group/radium/project-configuration](https://gitea.radium.group/radium/project-configuration) to a temporary directory. After all asynchronous tasks are complete, the script should compute the SHA-256 hashes for each file. The code must pass the `wemake-python-styleguide` linter without any issues. Configuration is available at [https://gitea.radium.group/radium/project-configuration](https://gitea.radium.group/radium/project-configuration). Ensure 100% test coverage.

## Questions and Answers

1. **How did you implement asynchronous task execution in your script?**

   Asynchronous task execution in the script was implemented using the `asyncio` library, which allows tasks to run concurrently without blocking the main execution thread. Main functions like `fetch_file_list`, `download_files`, `process_files`, and `main` were defined as `async` functions to enable asynchronous execution.

2. **What libraries were used to download the repository contents and for what purposes?**

   The following libraries were used:
   - **`aiohttp`**: Used for making asynchronous HTTP requests to load file lists and file contents from the repository.
   - **`aioresponses`**: Used to mock HTTP requests in tests to simulate server responses and verify the asynchronous code.

3. **What asynchronous issues did you encounter while performing the task and how did you resolve them?**

   Common asynchronous issues included:
   - **Concurrent Access to Resources**: Ensured proper handling of shared resources such as temporary files.
   - **Task Synchronization**: Made sure all tasks completed properly before the main function finished.
   - **Testing Asynchronous Code**: Required special testing methods such as using `aioresponses` and `AsyncMock` to simulate async operations.

   These issues were addressed by using appropriate libraries and tools for managing asynchronous tasks and testing.

4. **How did you organize the downloading of files to a temporary folder?**

   File downloading to a temporary folder was organized using the `pathlib` library for filesystem paths. Files were downloaded to a temporary directory provided by `pytest` through the `tmp_path` parameter. For each file, a complete path was created, and the file's contents were written to the respective path using the `write_bytes` method.

5. **What are the main `wemake-python-styleguide` requirements you find most important for maintaining code quality?**

   - **Clarity and Readability of Code**
     - **Maximum Line Length**: Code should not exceed 79 characters per line to avoid horizontal scrolling and improve readability.
     - **Function and Method Separation**: Each function or method should perform a single task, making the code more modular and testable.
     - **Naming Conventions**: Names should be descriptive and clear, such as `calculate_sha256` instead of `calc_sha`.
   - **Minimizing Complexity**
     - **Limitation on Local Variables**: A maximum of 5 local variables per function to reduce complexity and improve code readability. While limiting local variables helps reduce function complexity and improves testability, it may lead to other issues like complicating logic, increasing cognitive load, and excessive abstraction. It’s important to balance and apply this rule thoughtfully based on the context and specifics of the task.
     - **Limitation on Nesting**: The maximum nesting level should not exceed 4 to prevent complex and confusing structures.
   - **Explicit Constructs and Avoiding Magic**
     - **No Magic Numbers and Strings**: All numbers and strings used in the code should be declared as constants to avoid unexpected errors and improve code clarity.
     - **Explicit Return Values**: Functions should return values explicitly to clarify their purpose.
   - **Consistency and Formatting Standards**
     - **Docstrings**: All modules, classes, and functions should have docstrings to improve documentation and help other developers understand the code’s purpose and usage.
     - **Import Organization**: Imports should be ordered and separated into three groups: standard libraries, third-party libraries, and local modules.
   - **Security and Performance**
     - **Avoid Assert for Checking**: In production code, asserts may be disabled, so explicit checks and exceptions should be used instead.
     - **Avoid Eval and Exec**: These functions can be dangerous and lead to security vulnerabilities.
   - **Testability**
     - **Maximum Test Coverage**: The code should be as fully covered by tests as possible, including both unit tests and integration tests.
     - **Test Clarity**: Tests should be simple and understandable, avoiding complex logic in tests.

6. **How did you configure your project to meet the nitpick configuration mentioned in the task? Were there any difficulties in the configuration?**

   The project was configured to meet the nitpick configuration by creating and setting up configuration files such as `setup.cfg` and `.editorconfig`. Main difficulties included the need to accurately adjust the coding style to meet all `wemake-python-styleguide` rules and integrating these tools into the development process.

7. **What tools did you use to measure 100% test coverage?**

   The following tools were used:
   - **`pytest-cov`**: A pytest plugin that measures test coverage.
   - **`coverage.py`**: A library used by pytest-cov for detailed coverage reports.

8. **What types of tests did you write to verify the functionality of your script? (e.g., unit tests, integration tests)**

   - **Unit Tests**: These tests check individual functions and methods in isolation from other parts of the system. Tests were created for functions such as:
     - `fetch_file_list`
     - `download_files`
     - `process_files`
     - `calculate_sha256`
     - `split_list`
   - **Integration Tests**: These tests check the interaction between different parts of the system to ensure functions work together and process data correctly. Tests included:
     - Full execution scenario in the `main` function.
   - **Functional Tests**: These tests verify core functionalities from the perspective of end users, focusing on:
     - Correct downloading and saving of files.
     - Accurate computation and return of hashes.
   - **Asynchronous Tests**: These tests ensure asynchronous functions and methods work correctly with async tasks, using `aioresponses` and `AsyncMock` for simulation.

9. **How did you test asynchronous code? Did you use mocks or stubs for testing asynchronous operations?**

   Asynchronous code was tested using the `aioresponses` library for mocking HTTP requests and server responses. Additionally, `AsyncMock` from the `unittest.mock` library was used to mock asynchronous functions and methods. This allowed for effective simulation of various scenarios and verification of async code behavior.
