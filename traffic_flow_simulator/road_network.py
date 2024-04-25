
class RoadNetwork:

    def __init__(self, speed_limit=30, stop_sign=None, stop_duration=3, path=None, name=None, start=None, end=None, cars=None, intersect_roads=None) -> None:
        self.__speed_limit = speed_limit
        self.__stop_sign = stop_sign or []
        self.__name = name
        self.__path = path
        self.__start = start
        self.__end = end
        self.__cars = cars or []
        self.__stop_duration = stop_duration
        self.__intersect_roads = intersect_roads or []
    

    def get_intersections(self):

        """
        Function: returns a list of roads that intersect with the current RoadNetwork object

        Parameters: None

        Returns: 
            
            intersect_roads
                type: list[RoadNetwork]
        """
        return self.__intersect_roads
    
    def get_name(self):

        """
        Function: returns name of current RoadNetwork object

        Parameters: None

        Returns:

            name
                type: str
        """
        return self.__name
    
    def get_path(self):
        """
        Function: returns list of points of current RoadNetwork object

        Parameters: None

        Returns: 
            
            path
                type: list[tuple]
        """
        return self.__path
    
    def get_start(self):

        """
        Function: returns starting position of path

        Parameters: None

        Returns: 
            
            start
                type: tuple
        """
        return self.__start
    
    def get_end(self):

        """
        Function: returns ending position of path

        Parameters: None

        Returns: 
            
            end
                type: tuple
        """
        return self.__end
    
    def get_cars(self):

        """
        Function: returns list of Car objects present in current RoadNetwork object

        Parameters: None

        Returns: 
        
            cars
                type: list[Car]
        """
        return self.__cars
    
    def get_speed_limit(self):

        """
        Function: returns speed limit number of current RoadNetwork object

        Parameters: None

        Returns: 
            
            speed_limit
                type: float
        """
        return self.__speed_limit
    
    def get_stop_sign_pos(self):

        """
        Function: returns list of stop sign positions

        Parameters: None

        Returns:

            stop_sign
                type: list[tuple]
        """
        return self.__stop_sign
    
    def get_stop_duration(self):

        """
        Function: returns stop duration 

        Parameters: None

        Returns: 

            stop_duration
                type: float
        """
        return self.__stop_duration

    def add_car(self, car):

        """
        Function: appends Car object to cars list and sets Car object's path to RoadNetwork's path

        Parameters:

            car
                type: Car object
        
        Returns: None
        """
        car.set_current_pos(self.get_start())
        car.set_path(self.get_path())
        self.__cars.append(car)

    def has_stop_sign(self):
        
        """
        Function: returns boolean value of stop_sign list, if empty returns false else true

        Parameters: None

        Returns: 

            stop_sign:
                type: list[tuple]
        """
        return self.__stop_sign
    
    def temp_stop_cars(self):

        """
        Function: stops Car objects in cars list if Car object at stop sign

        Parameters: None

        Returns: None
        """ 

        if self.has_stop_sign():
        
            cars = self.get_cars()
            for car in cars:
                if car.get_current_pos() in self.get_stop_sign_pos() and not car.get_stop_state():
                    car.set_stop_state(True)
        
    def remove_any_end_cars(self):

        """
        Function: removes car in cars list if car at end position

        Parameters: None

        Returns: None
        """
        cars = self.get_cars()
        for car in cars:
            if car.get_current_pos() == self.get_end():
                self.remove_car(car)
    
    def detect_cars(self, current_pos, distance, intersect_roads=None): # function for a car to keep a following distance by finding any cars in certain distance

        """
        Function: checks for distance amount of grid blocks in front of Car object for Car objects.
        
        Parameters:

            current_pos:
                type: tuple
            
            distance:
                type: int
            
            intersect_roads:
                default: None
                type: list[RoadNetwork]

        Returns: 

            True: 
                if Car object found 
            
            False:
                if Car object not found

        """

        path = self.get_path()
        current_pos_ind = path.index(current_pos)
        pos_in_distance = []

        for i in range(1, distance+2):
            if (i + current_pos_ind) <= len(path)-1:      
                pos_in_distance.append(path[current_pos_ind+i])
        
        if not intersect_roads:
            intersect_roads = self.__intersect_roads
            for road in intersect_roads:
                cars = road.get_cars()
                for car in cars:
                    if car.get_current_pos() in pos_in_distance:
                        return True        
        
        for car in self.get_cars():
            if car.get_current_pos() in pos_in_distance:
                return True
            
        return False

    def remove_car(self, car_obj):

        """
        Function: removes Car object from cars list

        Parameters: 

            car_obj:
                type: Car object
        
        Returns: None
        """

        cars = self.get_cars()
        cars.remove(car_obj)

    def check_for_collisions(self):

        """
        Function: removes Car objects given a collisions dictionary and adds position of collision into block_to_color

        Parameters: None

        Returns: 
            
            blocks_to_color:
                type: list[tuple]
        """

        blocks_to_color = []
        collisions = self._check_for_collisions()

        for collision in collisions.values():
            if len(collision) < 2:
                continue
            else:
                for car, road in collision:
                    print(f'Removing car at pos {car.get_current_pos()} on road {road.get_name()}')
                    road.remove_car(car)
                    blocks_to_color.append(car.get_current_pos())
        return blocks_to_color



    def _check_for_collisions(self):

        """
        Function: finds collisions (when two Car objects have same current position) within the RoadNework and other RoadNetworks in intersect_roads

        Parameters: None

        Returns:

            collisions:
                type: dict{tuple: list[tuple]}
        """
        
        collisions = {}

        intersecting_roads = self.get_intersections()
        self_cars = self.get_cars()
        for car in self_cars:
            if car.get_current_pos() in collisions:
                collisions[car.get_current_pos()].add((car, self))
                print(f"Collision at {car.get_current_pos()}")
            else:
                collisions[car.get_current_pos()] = set([(car, self)])
        
        for road in intersecting_roads:
            for car in road.get_cars():
                if car.get_current_pos() in collisions:
                    collisions[car.get_current_pos()].add((car, road))
                    print(f"Collision at {car.get_current_pos()}")

        
        return collisions
        
        


if __name__ == "__main__":
    print("File is not meant run")

        

        

    


    
