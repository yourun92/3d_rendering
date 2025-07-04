import dxfgrabber
import svgwrite
import math

def get_bounding_box(entities):
    # Инициализируем границы с очень большими значениями
    min_x = min_y = 1e10
    max_x = max_y = -1e10
    
    for entity in entities:
        # Обрабатываем линии
        if hasattr(entity, 'start'):
            min_x = min(min_x, entity.start[0])
            min_y = min(min_y, entity.start[1])
            max_x = max(max_x, entity.start[0])
            max_y = max(max_y, entity.start[1])
            
        if hasattr(entity, 'end'):
            min_x = min(min_x, entity.end[0])
            min_y = min(min_y, entity.end[1])
            max_x = max(max_x, entity.end[0])
            max_y = max(max_y, entity.end[1])
            
        # Обрабатываем круги и дуги
        if hasattr(entity, 'center'):
            min_x = min(min_x, entity.center[0])
            min_y = min(min_y, entity.center[1])
            max_x = max(max_x, entity.center[0])
            max_y = max(max_y, entity.center[1])
            
            # Учитываем радиус для кругов и дуг
            if hasattr(entity, 'radius'):
                min_x = min(min_x, entity.center[0] - entity.radius)
                min_y = min(min_y, entity.center[1] - entity.radius)
                max_x = max(max_x, entity.center[0] + entity.radius)
                max_y = max(max_y, entity.center[1] + entity.radius)
        
        # Обрабатываем LWPOLYLINE и POLYLINE (набор вершин)
        if entity.dxftype in ('LWPOLYLINE', 'POLYLINE'):
            for point in entity.points if hasattr(entity, 'points') else entity.vertices:
                x, y = point[0], point[1]
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    
    # Если файл пустой, используем стандартные размеры
    if min_x == 1e10:
        min_x = 0
        min_y = 0
        max_x = 1000
        max_y = 1000
    
    return min_x, min_y, max_x, max_y

def dxf_to_svg(dxf_path, svg_path):
    dxf = dxfgrabber.readfile(dxf_path)
    
    # Получаем границы для масштабирования
    min_x, min_y, max_x, max_y = get_bounding_box(dxf.entities)
    width = max_x - min_x
    height = max_y - min_y
    
    # Создаем SVG с фиксированным размером
    dwg = svgwrite.Drawing(svg_path, 
                          size=("1000px", "1000px"),
                          viewBox=f"{min_x} {min_y} {width} {height}")

    for entity in dxf.entities:
        if entity.dxftype == 'LINE':
            dwg.add(dwg.line(
                start=(entity.start[0], -entity.start[1]),  # Инвертируем Y для SVG
                end=(entity.end[0], -entity.end[1]),
                stroke='black',
                stroke_width=0.1
            ))
            
        elif entity.dxftype == 'CIRCLE':
            dwg.add(dwg.circle(
                center=(entity.center[0], -entity.center[1]),
                r=entity.radius,
                stroke='black',
                fill='none',
                stroke_width=0.1
            ))
            
        elif entity.dxftype == 'ARC':
            # Конвертируем радиус в градусы для SVG
            start_angle = math.degrees(entity.start_angle)
            end_angle = math.degrees(entity.end_angle)
            
            # Создаем путь для дуги
            path = dwg.path(d=f"M {entity.center[0] + entity.radius} {-entity.center[1]} ")
            path.arc(
                r=(entity.radius, entity.radius),
                rotation=0,
                arc_flag=1 if end_angle - start_angle > 180 else 0,
                sweep_flag=1,
                x=entity.center[0] + entity.radius * math.cos(math.radians(end_angle)),
                y=-entity.center[1] - entity.radius * math.sin(math.radians(end_angle))
            )
            dwg.add(path)
            
        elif entity.dxftype in ('LWPOLYLINE', 'POLYLINE'):
            points = [(p[0], -p[1]) for p in (entity.points if hasattr(entity, 'points') else [v for v in entity.vertices])]
            dwg.add(dwg.polyline(points=points, stroke='black', fill='none', stroke_width=0.1))
            
    dwg.save()

# Пример использования
dxf_to_svg(r'svg\Mangra.dxf', r'svg\mangra_5310_090.svg')