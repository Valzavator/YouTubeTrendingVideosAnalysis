# Моніторингова система аналізу популярних відео сервісу YouTube
YouTube сьогодні є найбільшим веб-сайтом для хостингу різного жанру відео-контенту та однозначно тримає лідерську позицію як головна медіа платформа в світі. Загальна кількість користувачів платформи становить більше 1,3 млрд осіб. Кожну хвилину на YouTube завантажується 300 годин медіа контенту! Щодня проглядається майже 5 мільярдів відеороликів. YouTube отримує більше 30 мільйонів відвідувачів в день.

Отже, можна зробити висновок, що YouTube має глибокий вплив на суспільство цілого світу в усіх аспектах. Тому аналіз наборів даних даної платформи є досить інформативною та важливою задачею для компаній, що досліджують соціальні тенденції чи створюють прогнози майбутніх стратегічних бізнес-планів.

***Метою розробки даного проекту*** є збір та фільтрація статистики популярних відео сервісу YouTube, проведення інтелектуального аналізу даних на її основі та формування бізнес-звітів з метою надання корисної інформації для рекламних агентств та інвесторів.

АНАЛІЗ ІНСТРУМЕНТАРІЮ
----
***Мова програмування*** – Python 3.7.2.

***СУБД*** – MongoDB 4.0

***Бібліотеки для аналізу даних:***

- NumPy 
- Pandas  
- NLTK  
- WordCloud 
- Matplotlib
- seaborn 

ОПИС ПРОГРАМНОГО ЗАБЕЗПЕЧЕННЯ
----
Модульна організація програми:

![Modular program organization](/resource/analysis_result/example/program_organization.PNG "Modular program organization")

Програмне забезпечення моніторингової системи аналізу популярних відео сервісу YouTube має мінімалістичний консольний інтерфейс. Тому структура програмного забезпечення значно спрощується порівняно з веб-інтерфейсом. Як видно з рисунку загальна структура представляє собою модульну організацію, коли робота програми базується на взаємодії незалежних між собою частин (крім модуля відповідального за CLI, через який організована взаємодія решти модулів), які в свою чергу виконують конкретно визначений функціонал.

Всього структура даного програмного забезпечення складається з 16 python-файлів; файлу .env, який місить змінні оточення (API_KEY для YouTube Data API, HOST для підключення до сервера MongoDB, MONGODUMP_PATH та MONGORESTORE_PATH - шляхи у файловій системі до відповідних стандартних утиліт MongoDB для резервування та відновлення даних) та файлу country_codes.txt в якому описані коди країн з яких сервер, відповідальний за збір даних, буде регулярно проводити скрапінг.
