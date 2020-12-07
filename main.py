from world import World
from logger import Logger
import tkinter as tk
import time


class Main:

    params_file = 'params.txt'
    params = {}
    ant_world = None
    tk_root = tk.Tk()

    @staticmethod
    def run():
        Main.read_params()

        ant_world = World(Main.params)

        if Main.params['aufgabe'] == 1:
            ant_world.populate()
        if Main.params['aufgabe'] == 2:
            ant_world.populate_explorers()
            ant_world.populate_carriers()

        ant_world_logger = Logger(ant_world, Main.tk_root, Main.params['graphic_scale'], Main.params['aufgabe'])
        # ant_world_logger.get_curr_state()
        # ant_world_logger.print_curr_state()
        #
        # ant_world_logger.draw_curr_state()

        for i in range(Main.params['loops']):
            ant_world_logger.get_curr_state()
            ant_world_logger.print_curr_state()
            ant_world_logger.draw_curr_state()
            ant_world_logger.write_log()

            Main.tk_root.update_idletasks()
            Main.tk_root.update()
            # time.sleep(Main.params['wait'])

            if Main.params['aufgabe'] == 1:
                ant_world.simulate_cycle()
            if Main.params['aufgabe'] == 2:
                ant_world.simulate_cycle_explorer_carrier()

            #time.sleep(1)

        tk.mainloop()
        ant_world_logger.file.close()

    @staticmethod
    def read_params():
        file_obj = open(Main.params_file)
        for line in file_obj:
            name = line.partition(": ")[0]
            value = int(line.split(": ")[1])
            Main.params[name] = value
        file_obj.close()


if __name__ == "__main__":
    Main.run()