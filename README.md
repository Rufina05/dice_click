Константинова Руфина  
Вариант 1

## Структура проекта

```text
testare_1/
├── tests/
│   ├── conftest.py
│   ├── test_dice.py
│   └── test_dal.py
├── dice.py
├── db.py
├── dal.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 2. Описание проекта

Логика приложения разделена на три файла:

- `dice.py` — основная логика приложения и команды CLI.
- `db.py` — настройка базы данных.
- `dal.py` — работа с данными (Data Access Layer).

### Тесты

- `test_dice.py` — тестирование основной логики и CLI.
- `test_dal.py` — тестирование доступа к данным.
- `conftest.py` — общие фикстуры pytest (`session`, `isolated_files`).

## 3. Установка и запуск

### Создание виртуального окружения

```powershell
python -m venv venv
```

### Активация виртуального окружения

```powershell
.\venv\Scripts\Activate.ps1
```

### Установка зависимостей

```powershell
pip install -r requirements.txt
pip install -e .
```

## 4. Команды приложения

### Бросок костей

```powershell
dice roll
```

Бросить три кости с двадцатью гранями:

```powershell
dice roll --count 3 --sides 20
```

Краткая запись команды:

```powershell
dice roll -c 2 -s 1
```

### Просмотр статистики

Абсолютная статистика:

```powershell
dice stats --view abs
```

Относительная статистика:

```powershell
dice stats --view rel
```

Статистика по умолчанию:

```powershell
dice stats
```

## 5. Проверка качества кода

Форматирование кода:

```powershell
ruff format .
```

Проверка кода на ошибки и нарушения правил:

```powershell
ruff check .
```

## 6. Функциональность

- `dice roll` — бросает кости, выводит результат каждой кости и их сумму, сохраняет каждый выпавший результат в базу данных.
- `dice stats` — показывает, как часто выпадала каждая грань для каждого типа кости.

## 7. Хранение данных

- `stats.db` — база данных со статистикой бросков.
- `app.log` — файл журнала приложения.

Оба файла создаются в текущей рабочей папке при запуске приложения.