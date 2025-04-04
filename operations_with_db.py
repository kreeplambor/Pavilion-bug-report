import os
import sqlite3
from json import dumps, loads
from constants_of_db import db_name, commands_create_tables


class db:
    """ Класс для работы с базой данных.
        Объектом класса является таблица базы данных,
            название которой находиться в переменной db_name.
        Класс содержит 6 методов."""

    def __init__(self, table):
        '''Метод для создания объекта класса.
        Необходимо передать название таблицы.'''

        if not os.path.isfile(db_name):
            # создание всех таблиц
            commands = commands_create_tables
            for command in commands:
                self.execute(command)

        self.name = table
        self.columns = tuple(
            [column[0]
                for column in self.execute(
                    'SELECT name FROM pragma_table_info(?)',
                    (self.name, ), 'fetchall')])

    def insert(self, columns_list, values_list):
        '''Метод для добавления данных в таблицу.
        Необходимо передать списоки столбцов и величин.'''

        values = values_list

        columns_list = '(' + ', '.join(columns_list) + ')'
        values_list = '(' ', '.join('?' * len(values_list)) + ')'

        query = 'INSERT INTO ' + self.name
        query += ' ' + columns_list
        query = ' VALUES ' + values

        self.execute(query, values)

    def read(self, conditions=None, columns_list=['*'], fetch_type='fetchall',
             unique=False, addl_tab=None):
        '''Метод для чтения данных из таблицы.
        Можно не передавать переменные, тогда будут выведены все данные.
        Можно передать списоки условий, столбцов и fetch_type.'''

        columns_list = ', '.join(columns_list)

        query = 'SELECT' + (' DISTINCT ' if unique else ' ')
        query += columns_list
        query += ' FROM ' + self.name

        if addl_tab:
            if isinstance(addl_tab, (list, tuple)):
                query += ', '.join(addl_tab)
            else:
                query += f', {addl_tab}'

        if conditions:
            condition = ' AND '.join(conditions)
            query += ' WHERE ' + condition

        result = self.execute(query, None, fetch_type)
        return(result)

    def update(self, columns_list, values_list, conditions, directly=False):
        '''Метод для обновления данных в таблицу.
        Необходимо передать списки столбцов, величин и условий.'''

        '''if directly is True:
            pair_column_value = [
                columns_list[x] + ' = ' + values_list[x]
                for x in range(len(columns_list))]
        else:
            pair_column_value = [
                columns_list[x] + ' = ?'
                for x in range(len(columns_list))]'''

        pair_column_value = [
            columns_list[x] + ' = ' + values_list[x] if directly
            else columns_list[x] + ' = ?'
            for x in range(len(columns_list))]

        condition = ' AND '.join(conditions)

        query = 'UPDATE ' + self.name + ' SET '
        query += ', '.join(pair_column_value)
        query += ' WHERE ' + condition

        if directly:
            self.execute(query)
        else:
            self.execute(query, values_list)

    def delete(self, conditions):
        '''Метод для удаления данных из таблицы.
        Необходимо передать список условий.'''

        condition = ' AND '.join(conditions)

        query = 'DELETE FROM ' + self.name
        query += ' WHERE ' + condition

        self.execute(query)

    def execute(self, query, args=None, fetch_type=None):
        '''Метод для выполнения SQL запроса.
        Необходимо передать запрос.
        Можно передать аргументы и способ вывода данных.'''

        # print('query =', query)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if args:
            cursor.execute(query, args)
        else:
            cursor.execute(query)
        if fetch_type:
            fetch_types = {'fetchall': cursor.fetchall,
                           'fetchone': cursor.fetchone}
            result = fetch_types[fetch_type]()
            conn.close()
            return(result)
        else:
            conn.commit()
            conn.close()


def json_functions(func, variable):
    '''Функций для преобразования списков и словарей и json и наобарот.
    Принимает функцию(load/dumps) и переменную.'''
    if func == 'dumps':
        result = dumps(variable, ensure_ascii=False)
    else:
        if variable is not None:
            result = loads(variable)
        else:
            result = None
    return(result)
