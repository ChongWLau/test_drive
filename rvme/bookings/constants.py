from model_utils import Choices


CURRENT_TYPES = Choices(
    ("ac", "AC"),
    ("dc", "DC"),
)

ENGINE_TYPES = Choices(
    ('cng', 'CNG'),
    ('diesel', 'Diesel'),
    ('electric', 'Electric'),
    ('gasoline', 'Gasoline'),
    ('hybrid', 'Hybrid'),
    ('other', 'Other'),
)

KEY_OPERATIONS = Choices(
    ('create', 'Create'),
    ('update', 'Update'),
    ('pickup', 'Pick up'),
    ('putback', 'Put back'),
)

KEY_STATUSES = Choices(
    ('cancelled', 'Cancelled'),
    ('ended', 'Ended'),
    ('valid', 'Valid'),
)

VEHICLE_MANUFACTURERS = Choices(
    ('alfaromeo', 'Alfa Romeo'),
    ('audi', 'Audi'),
    ('bentley', 'Bentley'),
    ('bmw', 'BMW'),
    ('buick', 'Buick'),
    ('byd', 'BYD'),
    ('cadillac', 'Cadillac'),
    ('caterham', 'Caterham'),
    ('chevrolet', 'Chevrolet'),
    ('chrysler', 'Chrysler'),
    ('citroen', 'Citroen'),
    ('dacia', 'Dacia'),
    ('daewoo', 'Daewoo'),
    ('daihatsu', 'Daihatsu'),
    ('dodge', 'Dodge'),
    ('fiat', 'Fiat'),
    ('ford', 'Ford'),
    ('fso', 'FSO'),
    ('honda', 'Honda'),
    ('hyundai', 'Hyundai'),
    ('infinity', 'Infinity'),
    ('iveco', 'Iveco'),
    ('jaguar', 'Jaguar'),
    ('jeep', 'Jeep'),
    ('kia', 'Kia'),
    ('lada', 'Lada'),
    ('lancia', 'Lancia'),
    ('landrover', 'Land Rover'),
    ('lexus', 'Lexus'),
    ('mazda', 'Mazda'),
    ('mercedesbenz', 'Mercedes-Benz'),
    ('mia', 'Mia'),
    ('mini', 'Mini'),
    ('mitsubishi', 'Mitsubishi'),
    ('nissan', 'Nissan'),
    ('opel', 'Opel'),
    ('peugeot', 'Peugeot'),
    ('porsche', 'Porsche'),
    ('qoros', 'Qoros'),
    ('renault', 'Renault'),
    ('saab', 'Saab'),
    ('seat', 'SEAT'),
    ('skoda', 'Skoda'),
    ('smart', 'Smart'),
    ('ssangyong', 'Ssangyong'),
    ('subaru', 'Subaru'),
    ('suzuki', 'Suzuki'),
    ('tata', 'Tata'),
    ('tesla', 'Tesla'),
    ('toyota', 'Toyota'),
    ('volkswagen', 'Volkswagen'),
    ('volvo', 'Volvo'),
)
