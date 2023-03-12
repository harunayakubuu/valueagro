from trucks.truck import Truck


def truck(request):
    return {'truck': Truck(request)}