Константинова Руфина
Вариант 1

Структура проекта:
testare_1/
tests/
  conftest.py
  test_dice.py
  test_dal.py
dice.py
db.py
dal.py
pyproject.toml
requirements.txt
README.md

Логика приложения разделена на 3 файла:
dice.py — основная логика и команды CLI
db.py — настройка базы данных
dal.py — работа с данными

Тесты:
test_dice.py — тестирование основной логики и CLI
test_dal.py — тестирование доступа к данным
+
conftest.py — общие фикстуры pytest (session, isolated_files)

Комманды для запуска:
python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
pip install -e .

комманды для проверки:
$ dice roll
$ dice roll --count 3 --sides 20
$ dice roll -c 2 -s 1
$ dice stats --view abs
$ dice stats --view rel
$ dice stats


ruff format .
ruff check .

- `dice roll` — бросить кости, напечатать результат каждой кости и сумму,
  сохранить каждый выпавший результат в базу;
- `dice stats` — показать, как часто выпадала каждая грань для каждого типа
  кости.

Данные хранятся в файле `stats.db`, логи пишутся в `app.log`. Оба файла создаются в текущей папке при запуске.

