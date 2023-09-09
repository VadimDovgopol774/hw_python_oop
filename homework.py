from dataclasses import dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

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
        return ((self.action * Training.LEN_STEP) / Training.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(type(self).__name__,
                                    self.duration,
                                    self.get_distance(),
                                    self.get_mean_speed(),
                                    self.get_spent_calories()
                                    )
        return training_info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * Training.get_mean_speed(self)
                + Running.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_1 = 0.035
    COEFF_2 = 0.029
    COEFF_3 = 0.278
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_1 * self.weight
                + ((Training.get_mean_speed(self) * self.COEFF_3)**2
                 / (self.height / SportsWalking.SM_IN_M))
                * self.COEFF_2 * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SPEED_COEFF_1 = 1.1
    SPEED_COEFF_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((Swimming.get_mean_speed(self) + self.SPEED_COEFF_1)
                * self.SPEED_COEFF_2 * self.weight * self.duration)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: Dict[str, Type[Training]] = {'SWM': Swimming,
                                           'RUN': Running,
                                           'WLK': SportsWalking,
                                           }
    if workout_type not in workouts:
        raise KeyError('Неожиданное значение')
    return workouts[workout_type](*data)


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
