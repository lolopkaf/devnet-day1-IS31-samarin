# Day 1 Report — DevNet Sprint

## 1. Student

* Name: Артур Самарин
* Group: IS31
* GitHub repo: [вставить ссылку на репозиторий]
* Day1 Token: D1-IB-23-5b-18-59D1

## 2. NetAcad progress (Module 1)

* Completed items: 1.1 / 1.2 / 1.3 (изучены материалы и выполнены активности модуля)

* Screenshot(s):


## 3. VM evidence

Работа выполнялась на Windows через VS Code без использования DEVASC VM

* File: `artifacts/day1/env.txt` exists: Yes


## 4. Repo structure (must match assignment)

* `src/day1_api_hello.py` : Yes
* `tests/test_day1_api_hello.py` : Yes
* `schemas/day1_summary.schema.json` : Yes
* `artifacts/day1/summary.json` : Yes
* `artifacts/day1/response.json` : Yes

## 5. Что я изучил сегодня

* Создание GitHub-репозитория и работа с Git.
* Создание структуры проекта для DevNet задания.
* Работа с виртуальным окружением Python (venv).
* Установка и использование библиотек requests, pytest и jsonschema.
* Отправка HTTP GET запроса к REST API.
* Проверка работы программы с помощью unit-тестов.

## 6. Проблемы и решения

Problem:
В Windows PowerShell по умолчанию запрещено выполнение скриптов, поэтому не активировалось виртуальное окружение Python.

Fix:
Была изменена политика выполнения скриптов с помощью команды:

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

После этого виртуальное окружение было успешно активировано.




