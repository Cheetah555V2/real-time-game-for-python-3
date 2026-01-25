import math

class Angle:
    def __init__(self, degree: float) -> None:
        self.degree = degree
    
    def get_degree(self) -> float:
        return self.degree
    
    def get_radian(self) -> float:
        if self.degree != 0:
            return math.pi / 180 * self.degree
        else:
            return 0
    
    def rotate(self, degree) -> None:
        """
        This function rotate the angle counter-clock wise
        """
        self.degree += degree
        self.degree %= 360

    def cos(self) -> float:
        return math.cos(self.get_radian())

    def sin(self) -> float:
        return math.sin(self.get_radian())
    
    def tan(self) -> float:
        return math.tan(self.get_radian())

    def __str__(self) -> str:
        return str(self.degree)
    
    def __repr__(self) -> str:
        return str(self.degree)
    
    def __add__(self, other: object) -> float:
        try:
            return (self.degree + other.degree) % 360 # type: ignore
        except AttributeError:
            raise AttributeError("Arimatic operation needs to be between Angle object only")
    
    def __sub__(self, other: object) -> float:
        try:
            return (self.degree - other.degree) % 360 # type: ignore
        except AttributeError:
            raise AttributeError("Arimatic operation needs to be between Angle object only")
    

    

if __name__ == "__main__":
    x = Angle(180)
    y = 2
    print(x + y)