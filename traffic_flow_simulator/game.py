import pygame as pyg
from road_network import *
from constants import *
from car import *
import random
import time

class App:

    def __init__(self, file_path=None) -> None:
        self.screen = pyg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pyg.time.Clock()
        self.collisions = 0
        self.file_path = file_path
        self.start_time = time.time()
    
    
    def draw_grid(self):

        """
        Function: draws grid based structure onto surface given width and height

        Parameters: None

        Returns: None
        """

        self.screen.fill(BG_COLOR)
        
        for i in range(0, WIDTH//BLOCK_SIZE):
            for j in range(0, HEIGHT//BLOCK_SIZE):
                rect = (i*BLOCK_SIZE+BORDER_SIZE, j*BLOCK_SIZE+BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE)
                pyg.draw.rect(self.screen,  BLOCK_COLOR, rect)

        pyg.display.flip()
    
    def draw_legend(self):

        """
        Function: draws legend onto surface

        Parameters: None

        Returns: None
        """

        pyg.draw.rect(self.screen, BLOCK_COLOR, (LEGEND_BOX_X, LEGEND_BOX_Y, LEGEND_BOX_WIDTH, LEGEND_BOX_HEIGHT))
        for color, label, y_pos in [(STOP_SIGN_COLOR, 'Stop Sign', 10), (CAR_COLOR, 'Car', 40), (CRASH_COLOR, 'Car Crash', 70), (ROAD_COLOR, 'Road', 100)]:
            pyg.draw.rect(self.screen, color, (LEGEND_BOX_X + 5, y_pos + 5, 20, 20))
            font = pyg.font.SysFont(None, 20)
            text_surface = font.render(label, True, color)
            self.screen.blit(text_surface, (LEGEND_BOX_X + 30, y_pos))

        toggle_font = pyg.font.SysFont(None, 20)
        text_surface = toggle_font.render('Toggle Pause with p', True, ROAD_COLOR)
        self.screen.blit(text_surface, (LEGEND_BOX_X + 5, 130))


        pyg.display.flip()
            

    
    def draw_font_for_collisions(self):

        """
        Function: draws font object onto surface that displays the number of collisions
        
        Parameters: None

        Returns: None
        """

        font = pyg.font.SysFont(None, FONT_SIZE)
        text_surface = font.render(f'Number of Collisions: {self.collisions}', True, FONT_COLOR, FONT_COLOR_BG)
        self.screen.blit(text_surface, (0, 0))

        pyg.display.flip()
    
    def play_crash_sound(self, file_path):

        """
        Function: plays a crashing sound through computer speakers

        Parameters: 

            file_path: 
                type: str

        Returns: None
        """
        if file_path:
            pyg.mixer.music.load(file_path)
            pyg.mixer.music.play()
        else:
            print("File path not provided")


    def draw_stop_sign(self, column, row):

        """
        Function: draws stop signs onto grid based surface

        Parameters:

            column:
                type: int
            row:
                type: int
        
        Returns: None
        """

        if column and row:
            rect = (column*BLOCK_SIZE+BORDER_SIZE, row*BLOCK_SIZE+BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE)
            pyg.draw.rect(self.screen, STOP_SIGN_COLOR, rect)
            pyg.display.flip()


    def draw_roads(self, list_of_roads=[]):

        """
        Function: draws road networks onto grid based surface

        Parameters:

            list_of_paths:
                type: list[RoadNetwork]
        
        Returns: None
        """

        if list_of_roads:
            for Path in list_of_roads:
                if Path.get_path():
                    path = Path.get_path()

                    for pos in path:
                        rect = (pos[0]*BLOCK_SIZE+BORDER_SIZE, pos[1]*BLOCK_SIZE+BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE)
                        pyg.draw.rect(self.screen, ROAD_COLOR, rect)
                    
                    if Path.has_stop_sign():
                        for stop_sign in Path.get_stop_sign_pos():
                            x, y = stop_sign[0], stop_sign[1]
                            self.draw_stop_sign(x, y)
                else:
                    print("Path not provided for ", Path.get_name())

        pyg.display.flip()
    
    
    def draw_cars(self, list_of_roads=[]):

        """
        Function: draws cars onto grid based surface

        Parameters:

            list_of_roads:
                type: list[RoadNetwork]

        Returns: None
        """

        for road in list_of_roads:
            cars = road.get_cars()
            if cars:
                for car in cars:
                    pos = car.get_current_pos()
                    rect = (pos[0]*BLOCK_SIZE+BORDER_SIZE, pos[1]*BLOCK_SIZE+BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE)
                    pyg.draw.rect(self.screen, CAR_COLOR, rect)
        pyg.display.flip()

    
    def move_cars(self, list_of_roads=[]):

        """
        Function: moves every car from all roads if able up one position in their corresponding path.

        Parameters:

            list_of_roads:
                type: list[RoadNetwork]
        
        Returns: None
        """

        for road in list_of_roads:

            cars = road.get_cars()

            for car in cars:
                x, y = car.get_current_pos()
                if not road.detect_cars(car.get_current_pos(), car.get_following_distance()):
                    if car.move(road.get_stop_duration()):
                        rect = (x*BLOCK_SIZE+BORDER_SIZE, y*BLOCK_SIZE+BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE)
                        if (x, y) in road.get_stop_sign_pos(): #recolor stop sign when car leaves it
                            self.draw_stop_sign(x, y)
                        else: #recolor road when car leave
                            pyg.draw.rect(self.screen, ROAD_COLOR, rect)
                                




            blocks_to_color = road.check_for_collisions() #Check if any collisions have occured. If so, color blocks after collisions with road color

            if blocks_to_color:
                for block in blocks_to_color:
                    x, y = block[0], block[1]
                    rect = (x*BLOCK_SIZE+BORDER_SIZE, y*BLOCK_SIZE+BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE, BLOCK_SIZE-BORDER_SIZE)
                    pyg.draw.rect(self.screen, CRASH_COLOR, rect)
                self.collisions += 1
                self.play_crash_sound(self.file_path)
            
            road.remove_any_end_cars() #remove cars that are at end of road
            road.temp_stop_cars() #stop cars if they are at stopsign 
                

        pyg.display.flip()
            
    

    
    def check_for_intersections(self, list_of_roads):

        """
        Function: checks to see if any points are shared within roads. If so, updates the intersecting roads' intersect roads list

        Parameters:

            list_of_roads:
                type: list[RoadNetwork]
        """

        list_of_paths = [i.get_path() for i in list_of_roads]
        roads_of_intersections = []

        shared_elements = {}
        for i, sublist in enumerate(list_of_paths):
            for elem in sublist:
                if elem not in shared_elements:
                    shared_elements[elem] = set()
                shared_elements[elem].add(i)


        intersections = {elem: list(indices) for elem, indices in shared_elements.items() if len(indices) > 1}
        intersections = list(intersections.values())
        for elem in intersections:
            if elem not in roads_of_intersections:
                roads_of_intersections.append(elem)

        for intersection in roads_of_intersections:
            for i in intersection:
                for j in intersection:
                    if i == j:
                        continue
                    list_of_roads[i].get_intersections().append(list_of_roads[j])
    
    def spawn_cars(self, list_of_roads, percentage_of_slowed_cars=0.3):

        """
        Function: places cars at starting postitions of roads based upon rate (CAR_SPAWN_RATE). 
                  Also, randomly assigns no following distance to cars for collisions to occur

        Parameters:

            list_of_roads:
                type: list[RoadNetwork]
            
            percentage_of_slowed_cars:
                type: float
            

        Returns: None
        """
        elapsed_time = time.time()
        if elapsed_time - self.start_time >= CAR_SPAWN_RATE:

            is_slowed_reaction_time = random.randint(1, 100)
            road = random.choice(list_of_roads)
            if road.get_start() not in [car.get_current_pos() for car in road.get_cars()]:
                if is_slowed_reaction_time <= percentage_of_slowed_cars*100:
                    road.add_car(Car(velocity=road.get_speed_limit(), following_distance=NO_FOLLOWING_DISTANCE))
                else:
                    road.add_car(Car(velocity=road.get_speed_limit()))

            self.start_time = time.time()
            self.draw_font_for_collisions()


    def run(self):

        """
        Function: runs main game loop

        Parameters: None

        Returns: None
        """
        
        running = True
        roads=[]

        points1 = [(x, 21) for x in range(39, -1, -1)]
        road_1 = RoadNetwork(speed_limit=0.1, start=points1[0], end=points1[len(points1)-1], name='Highway 1', path=points1)
        roads.append(road_1)

        points2 = [(x, 22) for x in range(39, -1, -1)]
        road_2 = RoadNetwork(speed_limit=0.1, start=points2[0], end=points2[len(points2)-1], name='Highway 2', path=points2)
        roads.append(road_2)

        points3 = [(x, 23) for x in range(0, 40, 1)]
        road_3 = RoadNetwork(speed_limit=0.1, start=points3[0], end=points3[len(points3)-1], name='Highway 3', path=points3)
        roads.append(road_3)

        points4 = [(x, 24) for x in range(0, 40, 1)]
        road_4 = RoadNetwork(speed_limit=0.1, start=points4[0], end=points4[len(points4)-1], name='Highway 4', path=points4)
        roads.append(road_4)

        points5 = [(17, 0), (17, 1), (17, 2), (17, 3), (17, 4), (17, 5), (17, 6), (17, 7), (17, 8), (17, 9), (17, 10), (17, 11), (16, 12), (15, 13), (14, 14), (13, 15),
                    (12, 16), (11, 17), (10, 18), (9, 19), (8, 20), (7, 21), (6, 21), (5, 21), (4, 21), (3, 21), (2, 21), (1, 21), (0, 21)]
        road_5 = RoadNetwork(speed_limit=0.3, start=points5[0], end=points5[len(points5)-1], name='Yielding_road 1', path=points5, stop_sign=[points5[points5.index((8, 20))]])
        roads.append(road_5)

        points6 = [(17, 0), (17, 1), (17, 2), (17, 3), (17, 4), (17, 5), (17, 6), (17, 7), (17, 8), (17, 9), (17, 10), (17, 11), (18, 12), (19, 13), (20, 14), (21, 15), (22, 16), (23, 17),
                    (24, 18), (24, 19), (24, 20), (24, 21), (24, 22), (24, 23), (24, 24), (24, 25), (24, 26), (24, 27), (24, 28), (24, 29), (24, 30), (24, 31), (24, 32), (24, 33), (24, 34), (24, 35), (24, 36), (24, 37), (24, 38), (24, 39)]
        road_6 = RoadNetwork(speed_limit=0.3, start=points6[0], end=points6[len(points6)-1], name='Yielding_road 2', path=points6, stop_sign=[points6[points6.index((24,20))]])
        roads.append(road_6)

        points7 = [(0, 24), (1, 24), (2, 24), (3, 24), (4, 24), (5, 24), (6, 24), (7, 24), (8, 24), (9, 24), (10, 24), (11, 24), (12, 24), (13, 24), (14, 24), (15, 24), (16, 24), (17, 24), (18, 24), (19, 24), (20, 24), (21, 24), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24), (27, 24),
                    (28, 24), (29, 24), (30, 24), (31, 24), (32, 25), (33, 26), (34, 27), (34, 28), (34, 29), (34, 30), (34, 31), (35, 32), (36, 32), (37, 32), (38, 32), (39, 32)]
        road_7 = RoadNetwork(speed_limit=0.1, start=points7[0], end=points7[len(points7)-1], name="Exit_route 1", path=points7)
        roads.append(road_7)

        points8 = [(39, 21), (38, 21), (37, 21), (36, 21), (35, 21), (34, 21), (33, 21), (32, 21), (31, 21), (30, 21), (29, 21), (28, 21), (27, 21), (26, 21), (25, 21), (24, 21), (23, 21), (22, 21), (21, 21), (20, 21), (19, 21), (18, 21), (17, 21), (16, 21),
                    (15, 21), (14, 21), (13, 21), (12, 21), (11, 21), (10, 21), (9, 21), (8, 21), (7, 21), (6, 21), (5, 21), (4, 21), (3, 20), (2, 19), (2, 18), (2, 17), (2, 16), (2, 15), (2, 14), (1, 13), (0, 12)]
        road_8 = RoadNetwork(speed_limit=0.1, start=points8[0], end=points8[len(points8)-1], name="Exit_route 2", path=points8)
        roads.append(road_8)




        self.draw_grid()
        self.draw_legend()
        self.draw_roads(roads)
        self.draw_font_for_collisions()
        self.check_for_intersections(roads)


        while running:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    running = False
                if event.type == pyg.KEYDOWN and event.key == pyg.K_p:
                    print("Simulation has paused")
                    paused = True
                    while paused:
                        for event in pyg.event.get():
                            if event.type == pyg.KEYDOWN and event.key == pyg.K_p:
                                paused = False


            self.spawn_cars(roads)
            self.draw_cars(roads)
            self.move_cars(roads)

        pyg.quit()



if __name__ == "__main__":
    pyg.init()
    pyg.display.set_caption("Traffic Flow Simulator with Pygame")
    g = App(file_path='sounds/crash-6711.mp3')
    g.run()



#TODO: Finish commenting code