import m11022124

from m11022124.ebus_map import get_bus_info_go

stop_ids = get_bus_info_go('0161000900')
for stop_id in stop_ids:
    print(f"stop_id: {stop_id}")