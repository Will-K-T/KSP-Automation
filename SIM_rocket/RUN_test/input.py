import os

exec(open("Modified_data/realtime.py").read())
exec(open("Modified_data/rocket.dr").read())

crashed_event = trick.new_event()
crashed_event.condition(0, "dyn.rocket.hasCrashed == True")
crashed_event.condition_any()
crashed_event.set_cycle(0.1)
crashed_event.action(0, "trick.stop()")
crashed_event.activate()

trick.add_event_before(crashed_event, "dyn.rocket.state_integ")

dyn.rocket.pos[1] = 6366707.0195
dyn.rocket.vel[1] = 1000
dyn.rocket.vel[0] = 10000

#==================================
# Start the variable server client.
#==================================
varServerPort = 34059
trick.var_server_set_port(varServerPort)
RocketDisplay_path = "models/graphics/RocketDisplay.py"
if (os.path.isfile(RocketDisplay_path)):
    RocketDisplay_cmd = RocketDisplay_path + " " + str(varServerPort) + " &"
    print(RocketDisplay_cmd)
    os.system(RocketDisplay_cmd);
else:
    print('Oops! Can\'t find ' + RocketDisplay_path)
