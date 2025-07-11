from bs4 import BeautifulSoup

# Чтение SVG файла
with open('svg/Aquabarrier/def_seams/DSHL/DSHL-15-030.svg', 'r', encoding='utf-8') as f:
    svg = BeautifulSoup(f.read(), 'xml')  # Используем xml-парсер

# Находим элемент по ID
rect = svg.find('rect', {'id': 'cover_right'})

# Изменяем атрибуты
if rect:
    rect['width'] = '400'  # Меняем ширину
    rect['fill'] = '#ff0000'  # Меняем цвет заливки

# Сохранение изменений
with open('svg/Aquabarrier/def_seams/DSHL/DSHL-15-030-test.svg', 'w', encoding='utf-8') as f:
    f.write(str(svg))