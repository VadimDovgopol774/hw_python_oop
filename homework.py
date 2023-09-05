from typing import Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    SEC_IN_HOUR: int = 3600
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    CALORIES_1: int = 18
    CALORIES_2: float = 1.79

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_1 * self.get_mean_speed()
                    + self.CALORIES_2)
                    * self.weight / self.M_IN_KM
                    * (self.duration * self.MIN_IN_HOUR))
        return calories


class SportsWalking(Training):
    CALORIES_1: float = 0.035
    CALORIES_2: float = 0.029
    MIN_IN_HOUR: int = 60
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    LEN_STEP: float = 0.65

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_1 * self.weight
                    + ((self.get_mean_speed() * self.M_IN_KM
                        / self.SEC_IN_HOUR) ** 2 // self.height)
                    * self.CALORIES_2 * self.weight)
                    * (self.duration * self.MIN_IN_HOUR))
        return calories


class Swimming(Training):
    LEN_STEP: float = 1.38
    CALORIES_1: float = 1.1
    CALORIES_2: int = 2

    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_1)
                * self.CALORIES_2 * self.weight)

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, str] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)


main()
