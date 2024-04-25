import time

class Car:

    def __init__(self, velocity=1, path=None, current_pos=None, stopped=False, following_distance=2) -> None:

        self.__velocity = velocity #seconds to move one grid square
        self.__path = path
        self.__current_pos = current_pos
        self.start_time = time.time()
        self.__stopped = stopped
        self.__following_distance = following_distance
    
    def get_velocity(self):

        """
        Function: returns velocity of Car object

        Parameters: None

        Returns:

            velocity:
                type: float
        """
        return self.__velocity
    
    def get_path(self):

        """
        Function: returns path that Car object follows

        Parameters: None

        Returns: 

            path:
                type: list[tuple]
        """
        return self.__path
    
    def get_current_pos(self):

        """
        Function: returns current position of Car object

        Parameters: None

        Returns: 

            current_pos:
                type: tuple
        """
        return self.__current_pos
    
    def get_stop_state(self):

        """
        Function: returns if car is stopped

        Parameters: None

        Returns: 

            stop_state:
                type: boolean
        """
        return self.__stopped
    
    def get_following_distance(self):
        """
        Function: returns if car is stopped

        Parameters: None

        Returns: 

            stop_state:
                type: boolean
        """
        return self.__following_distance

    def set_velocity(self, vel):

        """
        Function: assigns velocity of Car object to vel

        Parameters:

            vel:
                type: float

        Returns: None
        """
        self.__velocity = vel

    def set_path(self, path):

        """
        Function: assigns path of Car object to path

        Parameters:

            path:
                type: list[tuple]

        Returns: None
        """
        self.__path = path

    def set_current_pos(self, pos):

        """
        Function: assigns current position of Car object to pos

        Parameters:

            pos:
                type: tuple

        Returns: None
        """
        self.__current_pos = pos

    def set_stop_state(self, bool):

        """
        Function: assigns stop state of Car object to bool

        Parameters:

            bool:
                type: boolean

        Returns: None
        """
        self.__stopped = bool

    
    def can_move(self):

        """
        Function: returns whether Car object can move on in path. 

        Parameters: None

        Returns:

            True:
                if Car object has current position, Car object is not at end position, and its time to move based upon velocity
            
            False:
                if at least one of conditions is False
        """

        end_time = time.time()
        elapsed_time = end_time - self.start_time
        current_pos = self.get_current_pos()
        path = self.get_path()
        current_pos_ind = path.index(current_pos)

        return self.get_current_pos() and current_pos_ind < len(path)-1 and elapsed_time >= self.__velocity

    def move(self, stop_duration=None):

        """
        Function: moves Car by one grid position within path if able or if Car's wait time == stop duration. 

        Parameters:

            stop_duration:

                type: float
        
        Returns:

            True:
                if Car moved
            
            False or None:
                if Car did not move
                
        """

        if self.can_move():

            end_time = time.time()
            elapsed_time = end_time - self.start_time
            current_pos = self.get_current_pos()
            path = self.get_path()
            current_pos_ind = path.index(current_pos)
            
            if self.get_stop_state() and stop_duration:
                if elapsed_time >= stop_duration: # if car waited long enough at stop sign
                    self.start_time = time.time()
                    new_pos_ind = current_pos_ind + 1
                    self.set_current_pos(path[new_pos_ind])
                    self.set_stop_state(False)
                    return True
            else:
                self.start_time = time.time()
                new_pos_ind = current_pos_ind + 1
                self.set_current_pos(path[new_pos_ind])
                return True
        else:
            return False
        
        

if __name__ == "__main__":
    print("File is not meant run")

                





    