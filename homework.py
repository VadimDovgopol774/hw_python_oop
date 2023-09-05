class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
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
        self.training_type = ''

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return ((self.action * Training.LEN_STEP) / Training.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        return info.get_message()


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        super().__init__(action, duration, weight)
        self.training_type = 'Бег'

    def get_spent_calories(self) -> float:
        return ((Running.CALORIES_MEAN_SPEED_MULTIPLIER
                * Training.get_mean_speed(self)
                + Running.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / Training.M_IN_KM
                * self.duration * Training.MIN_IN_H)


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
        self.training_type = 'Спортивная ходьба'

    def get_spent_calories(self) -> float:
        return ((SportsWalking.COEFF_1 * self.weight
                + ((Training.get_mean_speed(self) * SportsWalking.COEFF_3)**2
                 / (self.height / SportsWalking.SM_IN_M))
                * SportsWalking.COEFF_2 * self.weight)
                * self.duration * Training.MIN_IN_H)


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
        self.training_type = 'Плавание'

    def get_distance(self) -> float:
        return (self.action * Swimming.LEN_STEP / Training.M_IN_KM)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((Swimming.get_mean_speed(self) + Swimming.SPEED_COEFF_1)
                * Swimming.SPEED_COEFF_2 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pack_to_class = {'SWM': Swimming,
                     'WLK': SportsWalking,
                     'RUN': Running}
    return pack_to_class[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    return Training.show_training_info(training)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
