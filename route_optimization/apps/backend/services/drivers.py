from apps.backend.models import Driver, User

def create_driver(data: dict):
    user = User.objects.get(pk=data["user_id"])
    driver = Driver.objects.create(
        user=user,
        license_number=data.get("license_number"),
        is_active=data.get("is_active", True)
    )
    return driver

def update_driver(driver_id, data: dict):
    driver = Driver.objects.get(pk=driver_id)
    for field, value in data.items():
        setattr(driver, field, value)
    driver.save()
    return driver

def delete_driver(driver_id):
    driver = Driver.objects.get(pk=driver_id)
    driver.delete()
    return True

def get_driver(driver_id):
    return Driver.objects.get(pk=driver_id)

def get_all_drivers():
    return list(Driver.objects.all())
