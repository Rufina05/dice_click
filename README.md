Константинова Руфина
Вариант 1


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

Данные хранятся в файле `stats.db`, логи пишутся в `app.log`. Оба файла создаются в текущей папке при
запуске.

