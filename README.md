# Моніторингова система аналізу популярних відео сервісу YouTube
YouTube сьогодні є найбільшим веб-сайтом для хостингу різного жанру відео-контенту та однозначно тримає лідерську позицію як головна медіа платформа в світі. Загальна кількість користувачів платформи становить більше 1,3 млрд осіб. Кожну хвилину на YouTube завантажується 300 годин медіа контенту! Щодня проглядається майже 5 мільярдів відеороликів. YouTube отримує більше 30 мільйонів відвідувачів в день.

Отже, можна зробити висновок, що YouTube має глибокий вплив на суспільство цілого світу в усіх аспектах. Тому аналіз наборів даних даної платформи є досить інформативною та важливою задачею для компаній, що досліджують соціальні тенденції чи створюють прогнози майбутніх стратегічних бізнес-планів.

***Метою розробки даного проекту*** є збір та фільтрація статистики популярних відео сервісу YouTube, проведення інтелектуального аналізу даних на її основі та формування бізнес-звітів з метою надання корисної інформації для рекламних агентств та інвесторів.

---
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

---
ОПИС ПРОГРАМНОГО ЗАБЕЗПЕЧЕННЯ
----
###Модульна організація програми:

![Modular program organization](/resource/analysis_result/example/program_organization.PNG "Modular program organization")

Програмне забезпечення моніторингової системи аналізу популярних відео сервісу YouTube має мінімалістичний консольний інтерфейс. Тому структура програмного забезпечення значно спрощується порівняно з веб-інтерфейсом. Як видно з рисунку загальна структура представляє собою модульну організацію, коли робота програми базується на взаємодії незалежних між собою частин (крім модуля відповідального за CLI, через який організована взаємодія решти модулів), які в свою чергу виконують конкретно визначений функціонал.

Всього структура даного програмного забезпечення складається з 16 python-файлів; файлу .env, який місить змінні оточення (API_KEY для YouTube Data API, HOST для підключення до сервера MongoDB, MONGODUMP_PATH та MONGORESTORE_PATH - шляхи у файловій системі до відповідних стандартних утиліт MongoDB для резервування та відновлення даних) та файлу country_codes.txt в якому описані коди країн з яких сервер, відповідальний за збір даних, буде регулярно проводити скрапінг.

### Опис модулів програмного забезпечення
- ***Модуль відповідальний за Command Line Interface***

Відповідальний за взаємодію з користувачем програми. Забезпечує зв’язність решти модулів та комутує дані між ними. 

Всього в програмі налічується 4 меню для організації процеса аналізу популярних відео сервісу YouTube:

1. Головне меню – забезпечує переміщення між іншими меню інтерфейсу.

    ![main_menu.PNG](/resource/analysis_result/example/main_menu.PNG)
    
2. Меню конфігурації кодів країн – дозволяє користувачу налаштувати з якими країнами він збирається працювати (збирати дані чи аналізувати їх). Пункти меню: 1) власноруч вписати коди країн (система аналізує вхідні дані і не дозволить додати невалідні коди); 2) зчитати коди країн з файла (коди повинні бути записані окремо в нового рядку); 3) проаналізувати та отримати всі коди країн, дані яких вже наявні в базі; 4) виключно видалити; 5) видалити всі коди; 6) список існуючих кодів країн.

    ![codes_menu.PNG](/resource/analysis_result/example/codes_menu.PNG)

3. Меню управління базою даних – дозволяє користувачу проводити маніпуляції з базою даних, а саме: завантажити дані з YouTube Data API по сконфігурованим раніше кодам країн, завантажити дані з наявних датасетів, зробити резервну копію або відновити базу даних (використовується стандартні утиліти MongoDB – mongodump та mongorestore), очистити базу даних.

    ![db_menu.PNG](/resource/analysis_result/example/db_menu.PNG)
    
4. Меню аналізу даних – дає можливість користувачу вибрати яким чином проводити аналіз: окремо по кожній країні зі списку чи разом. Після проведення аналізу програми відкриває директорію розташування результатів в Провіднику системи.

    ![analysis_menu.PNG](/resource/analysis_result/example/analysis_menu.PNG)   

- ***Модуль відповідальний за збір даних***

Відповідальний за збір даних для подальшого аналізу. Модуль реалізовує два способи збору даних - актуальних в цей час через YouTube Data API та зібраних раніше та представлених в якості готового датасету. Також модуль містить окрему утиліту, яка використовуючи можливості цього ж модулю дозволяє регулярно збирати дані (1 раз на добу) у встановлений користувачем час.


- ***Модуль валідації та фільтрації даних***

Можливості модуля в основному використовуються при зборі даних, а саме для видалення надлишкових пробільних символів, для збору тегів відео в одну строку, для співставлення id категорії та власне жанра відео при збору даних з YouTube, для підготовки даних у разі їх збереження в .csv формат, а також для форматування датасетів.

- ***Модуль відповідальний за аналіз даних***

Містить перелік методів для аналізу даних. За допомогою бібліотек pandas, numpy, matplotlib, seaborn та WorldCloud будує відповідні графіки, хмари тегів, надає загальний тестовий аналіз. Детальніше з алгоритмами та результатами роботи можна ознайомитися в пункті 3.3. “Опис основних алгоритмів роботи” та в пунті 5. “Опис результатів аналізу предметної галузі”.

- ***Модуль бази даних (MongoDB)***

Відповідальний за взаємодію програми та бази даних MongoDB. Реалізовує функції з записом, зчиткою та видаленням даних, видачі результатів пошуку по кодам країн, а також для стоврення резервної копії та відновлення бази даних.

- ***Модуль допоміжних утиліт***

Містить функції зчитки даних з файлів (рядками та в форматі csv), а також запису даних (рядками чи в форматі csv). Також налаштовує взаємодію з аргументами командного рядка, та задає глобальні змінні для всієї програми (db_host, api_key, country_codes_path, raw_data_dir, category_id_file_path, analysis_res_dir, backup_db_dir). Користувач може власноруч задати значення цих змінних при запуску програми в терміналі.

![args.PNG](/resource/analysis_result/example/args.PNG)   

---
ОПИС РЕЗУЛЬТАТІВ АНАЛІЗУ ПРЕДМЕТНОЇ ГАЛУЗІ
----
Далі представлено графіки демонстрації результатів аналізу моніторингової системи аналізу популярних відео сервісу YouTube по США.

- На рисунку представлено графік нормального розподілу кількості переглядів, вподобань, неприхильності та коментарів. За ним можна переконатися у “адекватності” статистичних даних та визначити моду, медіану і середнє значення натурального логарифму вимірюваної величини (відповідає Х кординаті при найбільшому значенні У);

    ![normal_distribution.png](/resource/analysis_result/example/normal_distribution.png)

- На рисунку представлено графік кореляції між кількістю переглядів, вподобань, неприхильності та коментарів. Кореляція показує  зв’язок між двома кількісними змінними. Коефіцієнт кореляції показує ступінь, до якого дві змінні пов’язані (наскільки спільно чи подібно змінюються їх значення для різних спостережень). Навіть якщо дві змінні виглядають пов’язаними між собою, це не значить, що одна спричинила іншу. Так, можна побачити, що кількість вподобань і коментарів більше зростають з кількістю переглядів, чим неприхильність для аналізованих відео;

    ![correlation.png](/resource/analysis_result/example/correlation.png)

- На рисунку представлено графік співвідношення кількості відео в трендів по категоріям, де можна побачити, що більше половини контенту серед трендів складають відео з категорій Розваги та Музика;

    ![category_rating.png](/resource/analysis_result/example/category_rating.png)

- На рисунку представлено діаграми розмаху розподілу переглядів, вподобань, неприхильності та коментарів до відео по категоріям;

    ![distribution_boxplot.png](/resource/analysis_result/example/distribution_boxplot.png)

- На рисунку представлено графіки середнього рівня кількості переглядів, вподобань, неприхильності та коментарів у вигляді ламаної кривої. Вони менш інформативні ніж, наприклад, діаграми розмаху, але є більш інтуїтивно-зрозумілими для перегляду. Так можна побачити, що за кількістю переглядів категорія Музика значно випереджає інші, за вподобаннями - категорії Музика та Некомерційна діяльність, а за неприхильністю та кількістю коментарів - лише Некомерційна діяльність. Але тут криється проблема аналізу лише за середнім значенням кількості вимірюваної величини. Якщо звернутися до графіка співвідношення кількості відео в трендів по категоріям, то можна побачити, що Некомерційна діяльність зовсім не популярний жанр, також це видно з діаграми розмаху;

    ![distribution_plot.png](/resource/analysis_result/example/distribution_plot.png)

- На рисунку представлено гістограму середнього інтервалу в якому відео було в трендах. Як можемо бачити, в середньому відео перебувають в трендах від 1 до 7 днів;

    ![distribution_of_days_histogram.png](/resource/analysis_result/example/distribution_of_days_histogram.png)

- На рисунку представлено графік залежності кількості днів які відео було в трендах від категорії відео. Так, відео з категорії Шоу найдовше тримаються в трендах (до 11 днів);

    ![distribution_of_average_time.png](/resource/analysis_result/example/distribution_of_average_time.png)

- На рисунках представлено хмари тегів з найпопулярнішими словосполученнями серед тегів, назв відео та опису до відео відповідно;

    ![word_cloud_for_tags.png](/resource/analysis_result/example/word_cloud_for_tags.png "tags")
    
    ![word_cloud_for_titles.png](/resource/analysis_result/example/word_cloud_for_titles.png "titles")
    
    ![word_cloud_for_description.png](/resource/analysis_result/example/word_cloud_for_description.png "description")

- На рисунку представлено графік полярності настроїв відео по категоріям. Так, можна побачити, що в категоріях Новини і політика, Комедійні шоу та Ігри більше заперечень та негативної тональності у порівнянні з категоріями Стиль, Подорожі та Блоги, де переважає позитивна тональність.

    ![polarity_of_categories_ALL.png](/resource/analysis_result/example/polarity_of_categories_ALL.png)
