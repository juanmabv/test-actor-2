import pandas as pd

data = {
    'booleano': [True, False, False, True, True, False, False, True, False, False, True, False, True, False, True],
    'texto': ['Hola', 'Mundo', 'Python', 'Data', 'Science', 'OpenAI', 'ChatGPT', 'Pandas', 'DataFrame', 'Ejemplo', 'Columna', 'Número', 'Fecha', 'Hora', 'Datetime'],
    'entero': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    'decimal': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0, 11.1, 12.2, 13.3, 14.4, 15.5],
    'fecha': pd.date_range('2023-01-01', periods=15),
    'hora': pd.date_range('00:00:00', periods=15, freq='H'),
    'fecha_hora': pd.date_range('2023-01-01 00:00:00', periods=15, freq='H')
}

df = pd.DataFrame(data)


