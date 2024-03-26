from selenium.webdriver.chrome.options import Options

from entities.requests import DestinationRequest

import tempfile
import os

from folium import Map, Marker, PolyLine, Popup, Icon
from routingpy.routers import Graphhopper

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OpenStreetMapProvider:
    def __init__(self, graphhopper_token: str):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("window-size=1150,840")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Chrome(options=options)
        self.browser.fullscreen_window()

        self.router = Graphhopper(graphhopper_token)

    def take_screenshot(self, plot: Map) -> bytes:
        plot_html = plot.get_root().render()

        with tempfile.TemporaryFile(mode='w',
                                    delete=False,
                                    suffix='.html',
                                    encoding='utf-8') as temp_file:
            temp_file.write(plot_html)
            temp_file_path = temp_file.name

        self.browser.maximize_window()

        self.browser.get(f'file://{temp_file_path}')

        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "leaflet-tile-loaded")))

        os.remove(temp_file_path)

        return self.browser.get_screenshot_as_png()

    def __del__(self):
        self.browser.quit()

    def draw_plot(self,
                  destinations: list[DestinationRequest],
                  profile='car') -> Map:
        destinations = self.__convert_destinations_to_tuple__(destinations)

        # Определяем границы маршрута
        min_lat = min([point[1][0] for point in destinations])
        max_lat = max([point[1][0] for point in destinations])
        min_lon = min([point[1][1] for point in destinations])
        max_lon = max([point[1][1] for point in destinations])

        padding_lat = (max_lat - min_lat) * 0.1  # 10% отступа по широте
        padding_lon = (max_lon - min_lon) * 0.1  # 10% отступа по долготе

        # Reverse dimensions
        locations = [point[1][::-1] for point in destinations]

        # Route между origin и следующей точкой,
        # чтобы покрасить путь в #9b46f0
        route_origin_path = self.router.directions(locations=[locations[0], locations[1]],
                                                   profile=profile)

        route_path = self.router.directions(locations=locations[1:],
                                            profile=profile)

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
                    popup=Popup(destinations[i][0].split(',')[0],
                                show=True),
                    icon=Icon(color=color,
                              icon_color='white',
                              icon='flag'))
             .add_to(plot))

        route_origin_path = [path[::-1] for path in route_origin_path.geometry]
        route_path = [path[::-1] for path in route_path.geometry]

        # Draw origin route with #9b46f0 color
        PolyLine(locations=route_origin_path,
                 weight=4,
                 color='#FFD133',
                 opacity=0.7) \
            .add_to(plot)

        # Draw main route with black color
        PolyLine(locations=route_path,
                 weight=4,
                 color='black',
                 opacity=0.7) \
            .add_to(plot)

        return plot

    @staticmethod
    def __convert_destinations_to_tuple__(destinations: list[DestinationRequest]) -> list[tuple[str, []: float]]:
        return [(destination.name, [destination.lat, destination.lng]) for destination in destinations]