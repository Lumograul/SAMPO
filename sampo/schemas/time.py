from sampo.schemas.serializable import AutoJSONSerializable

TIME_INF = 2_000_000_000


# TODO Consider converting to StrSerializable
class Time(AutoJSONSerializable['Time']):
    """
    Class for describing all basic operations for working with time in framework

    :param value: initial time value
    """
    value: int
    
    def __init__(self, value: int = 0):
        """
        :param value: value of time
        """
        self.value = 0
        self.set_time(value)

    @staticmethod
    def inf():
        """
        Return very big time (tending to infinity)

        :return: object Time with infinity as value
        """
        return Time(TIME_INF)

    def __add__(self, other: 'Time' or int) -> 'Time':
        return Time(self.value + (other.value if isinstance(other, Time) else other))

    def __radd__(self, other: 'Time' or int) -> 'Time':
        return Time(self.value + (other.value if isinstance(other, Time) else other))

    def __sub__(self, other: 'Time' or int) -> 'Time':
        return Time(self.value - (other.value if isinstance(other, Time) else other))

    def __rsub__(self, other: 'Time' or int) -> 'Time':
        return Time((other.value if isinstance(other, Time) else other) - self.value)

    def __mul__(self, other: 'Time' or int) -> 'Time':
        return Time(self.value * (other.value if isinstance(other, Time) else other))

    def __rmul__(self, other: 'Time' or int) -> 'Time':
        return Time(self.value * (other.value if isinstance(other, Time) else other))

    def __floordiv__(self, other: 'Time' or int) -> 'Time':
        return Time(self.value // (other.value if isinstance(other, Time) else other))

    def __truediv__(self, other: 'Time' or int) -> float:
        return self.value / (other.value if isinstance(other, Time) else other)

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __eq__(self, other):
        return self.value == other

    def __bool__(self):
        return self.value != 0

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    def __unicode__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def set_time(self, value: int):
        value = int(value)
        if value > TIME_INF:
            value = TIME_INF
        elif value < -TIME_INF:
            value = -TIME_INF
        self.value = value

    def is_inf(self) -> bool:
        return abs(self.value) == TIME_INF
