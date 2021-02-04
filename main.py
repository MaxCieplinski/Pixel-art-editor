import pygame
import pickle

#Window settings
window_width = 1250
window_height = 700
background_colour = (160,160,160)
running = True
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Pixel art editor')
screen.fill(background_colour)

#Variables
cell_size = 9
cell_break = 1
grid_bool = True
grid_size = 64
row_delta = 1
column_delta = 1
yes = True
shading = False
selecting = False
change = True
picking = False
drag_start = None
drag_end = None
visited_pos = []
format_1_bool = False
format_2_bool = False
filling = False
colors_select = []
shade_value = 1.1
x_color_select_size = 50
y_color_select_size = 0
default_color = (255, 255, 255)
colors = [
(255, 255, 255),
(128, 128, 128),
(0, 0, 0),
(255, 0, 0),
(255, 255, 0),
(0, 255, 0),
(0, 0, 255),
(184, 3, 255),
(255, 165, 0),
(150, 75, 0),
(255, 204, 221),
(255, 215, 0),
(192, 192, 192),
(127, 225, 212),
(229, 43, 80),
(194, 178, 128),
(0, 255, 255),
(194, 178, 128),
(255, 0, 255),
(0, 0, 128),
(63, 0, 255),
(128, 0, 0),
(0, 255, 0),
(255, 0, 255),
(0, 128, 128),
(128, 128, 0),
(128, 0, 128),
(172, 225, 175),
(175,238,238),
(101,30,62)
]

color = (0, 0, 0)

#Classes
class Cell():
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.color = default_color
        self.selected = False

#Make a grid
grid = []
for row in range(grid_size):
    grid.append([])
    for column in range(grid_size):
        grid[row].append(Cell(cell_size))

#Draw color select
for i in colors:
    if window_height - y_color_select_size >= 0:
        color_select = pygame.draw.rect(screen, i, (window_width - x_color_select_size, window_height - y_color_select_size, 50, 50))
        if color_select not in colors_select:
            colors_select.append(color_select)
            colors_select.append(i)
        y_color_select_size += 50
    else:
        if yes:
            x_color_select_size += 50
            y_color_select_size_2 = 0
            yes = False
        if window_height - y_color_select_size_2 >= 0:
            color_select = pygame.draw.rect(screen, i, (window_width - x_color_select_size, window_height - y_color_select_size_2, 50, 50))
            if color_select not in colors_select:
                colors_select.append(color_select)
                colors_select.append(i)
            y_color_select_size_2 += 50

#Images
#<a target="_blank" href="https://icons8.com/icons/set/shade-selected-faces">Shade Selected Faces icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
shading_image = pygame.image.load(r'shade_icon.png') 
#<a target="_blank" href="https://icons8.com/icons/set/paint-bucket">Paint Bucket icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
bucket_image = pygame.image.load(r'bucket_icon.png')
#<a target="_blank" href="https://icons8.com/icons/set/save">Save icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
save_image = pygame.image.load(r'save_icon.png')
#<a target="_blank" href="https://icons8.com/icons/set/load-cargo">Load Cargo icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
load_image = pygame.image.load(r'load_icon.png')
#<a target="_blank" href="https://icons8.com/icons/set/select-none">Select None icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
select_image = pygame.image.load(r'select_icon.png')
#<a target="_blank" href="https://icons8.com/icons/set/color-dropper">Color Dropper icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
color_picker_image = pygame.image.load(r'color_picker_icon.png')
#<a target="_blank" href="https://icons8.com/icons/set/activity-grid--v1">Data Grid icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
grid_image = pygame.image.load(r'grid_icon.png')

#All points beetween two
def all_points(drag_start, drag_end):
    x = drag_start[0] - drag_end[0]
    y = drag_start[1] - drag_end[1]
    grid_points = []
    if x < 0:
        for x_point in range(drag_start[0], abs(x) + drag_start[0] + 1):
            if y < 0:
                for y_point in range(drag_start[1], abs(y) + drag_start[1] + 1):
                    grid_points.append([x_point, y_point])
            else:
                for y_point in range(drag_start[1] - abs(y), drag_start[1] + 1):
                    grid_points.append([x_point, y_point])
    else:
        for x_point in range(drag_start[0] - abs(x), drag_start[0] + 1):
            if y < 0:
                for y_point in range(drag_start[1], abs(y) + drag_start[1] + 1):
                    grid_points.append([x_point, y_point])
            else:
                for y_point in range(drag_start[1] - abs(y), drag_start[1] + 1):
                    grid_points.append([x_point, y_point])

    return grid_points

#Fill
def fill(grid, x, y, current_color, new_color):
    if grid[x][y].color != current_color:
        return
    if [x, y] in visited_pos:
        return

    visited_pos.append([x, y])
    grid[x][y].color = new_color
    moves = [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]
    for move in moves:
        fill(grid, move[0], move[1], current_color, new_color)

#Buttons
color_picker_button = pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 100, 50, 50))
screen.blit(color_picker_image, (window_width - 188, 112, 24, 24))
filling_button = pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 150, 50, 50))
screen.blit(bucket_image, (window_width - 188, 162, 24, 24))
shade_button = pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 200, 50, 50))
screen.blit(shading_image, (window_width - 188, 212, 24, 24))
format_0 = pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 250, 50, 50))
format_1 = pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 300, 50, 50))
format_2 = pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 350, 50, 50))
select_button = pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 400, 50, 50))
screen.blit(select_image, (window_width - 188, 412, 24, 24))
grid_button = pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 450, 50, 50))
screen.blit(grid_image, (window_width - 188, 462, 24, 24))
save_button = pygame.draw.rect(screen, (255, 255, 255), (window_width - 400, 350, 50, 50))
screen.blit(save_image, (window_width - 388, 362, 24, 24))
load_button = pygame.draw.rect(screen, (255, 255, 255), (window_width - 400, 400, 50, 50))
screen.blit(load_image, (window_width - 388, 412, 24, 24))
current_color_info = pygame.draw.rect(screen, color, (window_width - 400, 0, 50, 50))

#Program loop
while running:
    pygame.draw.rect(screen, color, (window_width - 400, 0, 50, 50))
    events = pygame.event.get()
    for event in events:
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False

        pos = pygame.mouse.get_pos()

        #Button click check
        if shade_button.collidepoint(pos):
            pygame.draw.rect(screen, (200, 200, 200), (window_width - 200, 200, 50, 50))
            screen.blit(shading_image, (window_width - 188, 212, 24, 24))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 200, 50, 50))
            screen.blit(shading_image, (window_width - 188, 212, 24, 24))

        if grid_button.collidepoint(pos):
            grid_button = pygame.draw.rect(screen, (200, 200, 200), (window_width - 200, 450, 50, 50))
            screen.blit(grid_image, (window_width - 188, 462, 24, 24))
        else:
            grid_button = pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 450, 50, 50))
            screen.blit(grid_image, (window_width - 188, 462, 24, 24))

        if format_0.collidepoint(pos):
            selecting = False
            filling = False
            shading = False
            format_1_bool = False
            format_2_bool = False

        if format_1.collidepoint(pos):
            selecting = False
            filling = False
            shading = False
            format_2_bool = False
            format_1_bool = True

        if format_2.collidepoint(pos):
            selecting = False
            filling = False
            shading = False
            format_1_bool = False
            format_2_bool = True

        if filling_button.collidepoint(pos):
            pygame.draw.rect(screen, (200, 200, 200), (window_width - 200, 150, 50, 50))
            screen.blit(bucket_image, (window_width - 188, 162, 24, 24))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 150, 50, 50))
            screen.blit(bucket_image, (window_width - 188, 162, 24, 24))

        if select_button.collidepoint(pos):
            pygame.draw.rect(screen, (200, 200, 200), (window_width - 200, 400, 50, 50))
            screen.blit(select_image, (window_width - 188, 412, 24, 24))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 400, 50, 50))
            screen.blit(select_image, (window_width - 188, 412, 24, 24))

        if save_button.collidepoint(pos):
            pygame.draw.rect(screen, (200, 200, 200), (window_width - 400, 350, 50, 50))
            screen.blit(save_image, (window_width - 388, 362, 24, 24))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (window_width - 400, 350, 50, 50))
            screen.blit(save_image, (window_width - 388, 362, 24, 24))

        if load_button.collidepoint(pos):
            pygame.draw.rect(screen, (200, 200, 200), (window_width - 400, 400, 50, 50))
            screen.blit(load_image, (window_width - 388, 412, 24, 24))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (window_width - 400, 400, 50, 50))
            screen.blit(load_image, (window_width - 388, 412, 24, 24))

        if color_picker_button.collidepoint(pos):
            pygame.draw.rect(screen, (200, 200, 200), (window_width - 200, 100, 50, 50))
            screen.blit(color_picker_image, (window_width - 188, 112, 24, 24))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (window_width - 200, 100, 50, 50))
            screen.blit(color_picker_image, (window_width - 188, 112, 24, 24))

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            column = pos[0] // cell_size
            row = pos[1] // cell_size
            if selecting:
                change = True
                drag_start = [row, column]
                drag_start = [row, column]

            if selecting == False and picking == False:
                for idx, i in enumerate(colors_select):
                    try:
                        if i.collidepoint(pos):
                            color = colors_select[idx + 1]
                            shading = False
                    except:
                        pass

            if picking:
                try:
                    color = grid[row][column].color
                except:
                    pass

            #Button click check
            if grid_button.collidepoint(pos):
                grid_bool = False

            if shade_button.collidepoint(pos):
                selecting = False
                filling = False
                format_1_bool = False
                format_2_bool = False
                picking = False
                shading = True

            if format_0.collidepoint(pos):
                selecting = False
                filling = False
                shading = False
                format_1_bool = False
                picking = False
                format_2_bool = False

            if format_1.collidepoint(pos):
                selecting = False
                filling = False
                shading = False
                format_2_bool = False
                picking = False
                format_1_bool = True

            if format_2.collidepoint(pos):
                selecting = False
                filling = False
                shading = False
                format_1_bool = False
                picking = False
                format_2_bool = True

            if filling_button.collidepoint(pos):
                selecting = False
                shading = False
                format_1_bool = False
                format_2_bool = False
                picking = False
                filling = True

            if select_button.collidepoint(pos):
                shading = False
                format_1_bool = False
                format_2_bool = False
                filing = False
                picking = False
                selecting = True

            if color_picker_button.collidepoint(pos):
                shading = False
                format_1_bool = False
                format_2_bool = False
                filing = False
                selecting = False
                picking = True

            #Save/Load
            if save_button.collidepoint(pos):
                with open('saves', 'wb') as file:
                    pickle.dump(grid, file)
            if load_button.collidepoint(pos):
                try:
                    with open('saves', 'rb') as file:
                        grid = pickle.load(file)
                except:
                    pass

            #Format_1
            try:
                if format_1_bool:
                    grid[row][column + 1].color = color
                    grid[row][column - 1].color = color
                    grid[row + 1][column].color = color
                    grid[row - 1][column].color = color
                elif format_2_bool:
                    grid[row][column + 1].color = color
                    grid[row][column - 1].color = color
                    grid[row + 1][column].color = color
                    grid[row - 1][column].color = color
                    grid[row + 1][column + 1].color = color
                    grid[row + 1][column - 1].color = color
                    grid[row - 1][column - 1].color = color
                    grid[row - 1][column + 1].color = color
            except:
                pass

            #Filling
            try:
                if filling:
                    fill(grid, row, column, grid[row][column].color, color)
            except IndexError:
                pass

            try:
                #Shading
                if shading:
                    if pressed[pygame.K_LSHIFT]:
                        color_test = (grid[row][column].color[0] / shade_value, grid[row][column].color[1] / shade_value, grid[row][column].color[2] / shade_value)
                    else:
                        color_test = (grid[row][column].color[0] * shade_value, grid[row][column].color[1] * shade_value, grid[row][column].color[2] * shade_value)
                    if color_test[0] >= 0 and color_test[0] <= 255 and color_test[1] >= 0 and color_test[1] <= 255 and color_test[2] >= 0 and color_test[2] <= 255:
                        color = color_test

                #Setting cell color
                if selecting == False:
                    grid[row][column].color = color
            except:
                pass

            pygame.event.wait()

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            column = pos[0] // cell_size
            row = pos[1] // cell_size
            if selecting:
                change = False
                drag_end = [row, column]

            pygame.event.wait()

        if pygame.mouse.get_pressed()[1]:
            pos = pygame.mouse.get_pos()
            column = pos[0] // cell_size
            row = pos[1] // cell_size

            try:
                grid[row][column].color = (255, 255, 255)
                print("Click ", pos, "Grid coordinates: ", row, column)
            except:
                pass

    try:
        if selecting:
            if drag_start is not None and drag_end is not None:
                points = all_points(drag_start, drag_end)
            for point in points:
                grid[point[0]][point[1]].selected = True
    except:
        pass

    for row in range(grid_size):
        for column in range(grid_size):
            pygame.draw.rect(screen, grid[row][column].color, [cell_size * column, cell_size * row, cell_size, cell_size])
            if selecting:
                if grid[row][column].selected:
                    pygame.draw.rect(screen, (0, 0, 0), [cell_size * column, cell_size * row, cell_size, cell_size], 1)
                if change:
                    grid[row][column].selected = False

            if grid_bool:
                pygame.draw.line(screen, (0, 0, 0), (0, column * cell_size), (600, column * cell_size), cell_break)

        if grid_bool:
            pygame.draw.line(screen, (0, 0, 0), (row * cell_size, 0), (row * cell_size, 1000), cell_break)

    pygame.time.delay(60)
    pygame.display.flip()


pygame.quit()