import tracker as tr

model, cap, size = tr.tracker_init()
result = tr.tracker_save(size)

tr.track_objects(model, cap, size, result)