class Dijkstra:
    def start(self, maze, colour_points_between, colour_point):
        # all possible points which it has seen, and it could go to!
        # all points here are UNVISITED
        visible = []
        # every point which has been the focus point in the loop
        visited = [maze.start_point]
        # print(f"START POINT: ({maze.start_point.x}, {maze.start_point.y})")
        selected_point_to_visit = maze.start_point

        total_g_value_so_far = 0  # g value is movement cost
        x = 0
        while selected_point_to_visit != maze.end_point:
            x += 1
            # print(f"############################# ITERATION {x}")
            # print(f"> VISITING: {(selected_point_to_visit.x, selected_point_to_visit.y)}")
            # print(f"> G VALUE (so far): {total_g_value_so_far}")
            # print(f"> #VISIBLE: {len(visible)}")

            colour_point(selected_point_to_visit, "pink", fps=10)
            for i in selected_point_to_visit.connections:  # calculate g value of surrounding nodes
                gvalue = i[1] + total_g_value_so_far
                visible_junction = i[0]
                if visible_junction not in visited:
                    # if a junction is already visible
                    # point A
                    # overwrite came_from to point B
                    visible_junction.came_from = selected_point_to_visit
                    INFORMATION = [visible_junction, gvalue]
                    # print(f"+ ADDING: {(visible_junction.x, visible_junction.y)} (g value: {gvalue})")
                    visible.append(INFORMATION)
                    colour_points_between(selected_point_to_visit, visible_junction, "cyan")
                    colour_point(visible_junction, "blue", fps=10)
                elif visible_junction == maze.end_point:
                    break

            smallest_g = min(visible, key=lambda INFO: INFO[1])
            visible.remove(smallest_g)
            visited.append(selected_point_to_visit)
            selected_point_to_visit = smallest_g[0]
            total_g_value_so_far = smallest_g[1]

            # print(total_g_value_so_far)
            # print(smallest_g, ">>>> this is the smallest distance to next junction or dead end and also contains the name of the next junction")
            # print(f"NEXT POINT: ({selected_point_to_visit.x}, {selected_point_to_visit.y})")

        # print("####### SUCCESS!!!! ######")
        # print("distance: "+str(total_g_value_so_far))

        current = maze.end_point
        while current.came_from != maze.start_point:
            # colour between current and current.came_from
            colour_points_between(current, current.came_from, "navy", 20)
            current = current.came_from
        colour_points_between(current, maze.start_point, "navy", 20) # TO WRITE ABOUT - wouldnt colour the very last section in navy


from maze_generate import generate_maze


class A_star:
    def heuristic(self, point, end_point):
        distance = ((point.x - end_point.x) ** 2 + (point.y - end_point.y) ** 2) ** 0.5
        return distance

    def start(self, maze, colour_points_between, colour_point):
        # all possible points which it has seen, and it could go to!
        # all points here are UNVISITED
        visible = []

        # every point which has been the focus point in the loop
        visited = [maze.start_point]
        # print(f"START POINT: ({maze.start_point.x}, {maze.start_point.y})")

        selected_point_to_visit = maze.start_point
        total_g_value_so_far = 0
        # x = 0

        while selected_point_to_visit != maze.end_point:
            # x += 1
            # print(f"############################# ITERATION {x}")
            # print(f"> VISITING: {(selected_point_to_visit.x, selected_point_to_visit.y)}")
            # print(f"> G VALUE (so far): {total_g_value_so_far}")
            # print(f"> #VISIBLE: {len(visible)}")

            colour_point(selected_point_to_visit, "pink", fps=5)
            for i in selected_point_to_visit.connections:  # calculate g value of surrounding nodes
                visible_junction = i[0]
                gvalue = i[1] + total_g_value_so_far  # HOW FAR IT HAS COME
                hvalue = A_star.heuristic(self, visible_junction, maze.end_point)  # HOW FAR THERE IS LEFT (approximately)
                fvalue = gvalue + hvalue
                if visible_junction not in visited:
                    visible_junction.came_from = selected_point_to_visit
                    INFORMATION = [visible_junction, gvalue, fvalue]
                    # print(f"+ ADDING: {(visible_junction.x, visible_junction.y)} (g value: {gvalue})")
                    visible.append(INFORMATION)
                    colour_points_between(selected_point_to_visit, visible_junction, "cyan")
                    colour_point(visible_junction, "blue", fps=10)
                elif visible_junction == maze.end_point:
                    break

            smallest_f = min(visible, key=lambda INFO: INFO[-1])  # INFO[-1] is the f value
            visible.remove(smallest_f)
            visited.append(selected_point_to_visit)
            selected_point_to_visit = smallest_f[0]
            total_g_value_so_far = smallest_f[1]

            # print(total_g_value_so_far)
            # print(smallest_f, ">>>> this is the smallest distance to next junction or dead end and also contains the name of the next junction")
            # print(f"NEXT POINT: ({selected_point_to_visit.x}, {selected_point_to_visit.y})")

        # print("####### SUCCESS!!!! ######")
        # print("distance: " + str(total_g_value_so_far))

        current = maze.end_point
        while current.came_from != maze.start_point:
            # colour between current and current.came_from
            colour_points_between(current, current.came_from, "navy", 20)
            current = current.came_from
        colour_points_between(current, maze.start_point, "navy", 20)
        # TO WRITE ABOUT - wouldnt colour the very last section in navy
