import tracker as tr
import menubar_vars as mnvs


model, cap, size = tr.tracker_init()
result = tr.tracker_save(size)

tr.track_objects(model, cap, size, result, classPerson=1)