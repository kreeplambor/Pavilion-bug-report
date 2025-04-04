db_name = 'магазин.db'

commands_create_tables = [
    '''CREATE TABLE IF NOT EXISTS Товары (
             ID_товара INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             Категория TEXT NOT NULL,
             Производитель TEXT NOT NULL,
             Название TEXT NOT NULL,
             Описание TEXT DEFAULT '-' NOT NULL,
             Изображение TEXT DEFAULT '-' NOT NULL,
             Модификации TEXT DEFAULT '[]' NOT NULL
               CHECK
               (json_array_length(Модификации) = json_array_length(Штрихкоды)),
             Штрихкоды TEXT DEFAULT '[]' NOT NULL,
             Количество_товаров_каждой_модификации TEXT DEFAULT '[]' NOT NULL
               CHECK
               (json_array_length(Количество_товаров_каждой_модификации) =
                json_array_length(Штрихкоды)),
             Количество_товара INTEGER DEFAULT 0,
             Цена INTEGER NOT NULL DEFAULT 100);''',

    '''CREATE TABLE IF NOT EXISTS Заказы (
             ID_заказа INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             Дата_заказа TEXT NOT NULL,
             Статус_заказа TEXT NOT NULL,
             Способ_получения TEXT NOT NULL,
             ID_клиента INTEGER NOT NULL,
             Список_товаров TEXT NOT NULL,
             FOREIGN KEY (ID_клиента) REFERENCES Клиенты(ID_клиента)
                ON UPDATE CASCADE
                ON DELETE SET NULL);''',

    '''CREATE TABLE IF NOT EXISTS Клиенты (
             ID_клиента INTEGER PRIMARY KEY NOT NULL,
             Мессенджер TEXT NOT NULL DEFAULT 'telegram',
             Имя TEXT NOT NULL,
             Никнейм TEXT NOT NULL,
             Номер_телефона INTEGER NOT NULL,
             Корзина TEXT DEFAULT '[]' NOT NULL);''',

    '''CREATE TABLE IF NOT EXISTS Скидки (
             ID_скидки INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             ID_товара INTEGER NOT NULL,
             Процент_скидки REAL NOT NULL,
             Дата_начала_скидки TEXT NOT NULL,
             Дата_окончания_скидки TEXT NOT NULL,
             FOREIGN KEY (ID_товара) REFERENCES Товары(ID_товара)
                ON UPDATE CASCADE
                ON DELETE CASCADE);''',

    '''CREATE VIEW IF NOT EXISTS Товары_со_скидками AS
            SELECT t.ID_товара,
                   t.Категория,
                   t.Производитель,
                   t.Название,
                   t.Описание,
                   t.Изображение,
                   (SELECT json_group_array(m.value)
                    FROM json_each(t.Модификации) m
                    JOIN json_each(t.Количество_товаров_каждой_модификации) k
                        ON m.rowid = k.rowid
                    WHERE k.value != 0) AS Модификации,
                   (SELECT json_group_array(sh.value)
                    FROM json_each(t.Штрихкоды) sh
                    JOIN json_each(t.Количество_товаров_каждой_модификации) k
                        ON sh.rowid = k.rowid
                    WHERE k.value != 0) AS Штрихкоды,
                   (SELECT json_group_array(value)
                    FROM json_each(t.Количество_товаров_каждой_модификации)
                    WHERE CAST (value AS INTEGER) > 0)
                    AS Количество_товаров_каждой_модификации,
                   t.Количество_товара,
                   CASE WHEN s.Процент_скидки IS NOT NULL AND
                      s.Дата_начала_скидки <= strftime('%d.%m.%Y', 'now') AND
                      s.Дата_окончания_скидки > strftime('%d.%m.%Y', 'now')
                   THEN t.Цена * (1 - s.Процент_скидки)
                   ELSE t.Цена
                   END AS Цена
            FROM Товары t
            LEFT JOIN Скидки s
                   ON t.ID_товара = s.ID_товара
            WHERE t.Количество_товара != 0;''']
tables_names = ['Товары', 'Заказы', 'Клиенты', 'Скидки', 'Товары_со_скидками']
columns_json = {
    tables_names[0]: [
        'Модификации', 'Штрихкоды', 'Количество_товаров_каждой_модификации'],
    tables_names[1]: ['Список_товаров'],
    tables_names[2]: ['Корзина'],
    tables_names[4]: [
        'Модификации', 'Штрихкоды', 'Количество_товаров_каждой_модификации']}

# Содержит название таблицы с товарами и дополнительные параметры.
products_table = [tables_names[4], {
    'categories': ['Устройства', 'Одноразки', 'Солевые жидкости'],
    'columns_for_user_choice': [
        'Категория', 'Производитель', 'Цена', 'Модификации'],
    'columns_for_products_list': [
        'Производитель', 'Название', 'Цена', 'ID_товара'],
    'columns_for_product_info': [
        'Производитель', 'Название', 'Описание', 'Изображение',
        'Модификации', 'Штрихкоды'],
    # 'price_categories': {},
    'modifications_name': {'Устройства': 'Цвета', 'Одноразки': 'Вкусы',
                           'Солевые жидкости': 'Вкусы'},
    'column_for_prodID': 'ID_товара',
    'column_for_price': 'Цена',
    'column_for_modifications': 'Модификации',
    'column_for_quantity': 'Количество_товара',
    'column_for_quantity_of_modifications':
        'Количество_товаров_каждой_модификации',
    'column_for_barcodes': 'Штрихкоды'}]

# Содержит название таблицы с клиентами и дополнительные параметры.
clients_table = [tables_names[2], {
    'column_for_clientID': 'ID_клиента',
    'column_for_messenger': 'Мессенджер',
    'column_for_card': 'Корзина',
    'columns_for_add_client': [
        'ID_клиента', 'Мессенджер', 'Имя', 'Никнейм']}]
