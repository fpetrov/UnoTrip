import tempfile
import os

from folium import Map, Marker, PolyLine, Popup, Icon
from routingpy.routers import Graphhopper

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

API_KEY = 'ed83a659-67df-473e-aa47-7bfb2a4907dd'

destinations = [
    ('Центральная художественная школа', [55.731876, 37.607434]),
    ('Музей Москвы', [55.736390, 37.593595]),
    ('Ресторан Mushrooms', [55.738748, 37.615088]),
    ('Париж', [48.856663, 2.351556])
]

# Определяем границы маршрута
min_lat = min([point[1][0] for point in destinations])
max_lat = max([point[1][0] for point in destinations])
min_lon = min([point[1][1] for point in destinations])
max_lon = max([point[1][1] for point in destinations])

padding_lat = (max_lat - min_lat) * 0.1  # Например, 10% отступа по широте
padding_lon = (max_lon - min_lon) * 0.1  # Например, 10% отступа по долготе

# Reverse dimensions
locations = [point[1][::-1] for point in destinations]

router = Graphhopper(api_key=API_KEY)

route_path = router.directions(locations=locations,
                               profile='car')

plot = Map(location=[0, 0],
           zoom_start=10)

plot.fit_bounds(bounds=[
    [min_lat - padding_lat, min_lon - padding_lon],
    [max_lat + padding_lat, max_lon + padding_lon]
])

# Mark all locations
for i, point in enumerate(locations):
    color = 'black'

    if i == 0:
        color = 'green'

    if i == len(locations) - 1:
        color = 'red'

    (Marker(point[::-1],
           radius=10,
           popup=Popup(destinations[i][0],
                       show=True),
           icon=Icon(color=color,
                     icon_color='white',
                     icon='flag'))
     .add_to(plot))

route_path = [path[::-1] for path in route_path.geometry]

# Draw route with #9b46f0 color
PolyLine(locations=route_path,
         weight=4,
         color='black',
         opacity=0.7)\
    .add_to(plot)

# plot.save('map.html')

# Open in browser
plot_html = plot.get_root().render()

with tempfile.TemporaryFile(mode='w',
                            delete=False,
                            suffix='.html',
                            encoding='utf-8') as temp_file:
    temp_file.write(plot_html)
    temp_file_path = temp_file.name
    image_name = os.path.basename(temp_file_path)

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(f'file://{temp_file_path}')

wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "leaflet-tile-loaded")))

driver.save_screenshot(f'screenshots/{image_name[:-5]}.png')

os.remove(temp_file_path)

input("Press Enter to continue...")