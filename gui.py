from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import waste_distance
from waste_distance import *

scale_value = 50

"""
This method will take the ordered list of nodes we traverse, and draw lines for the path that is taken
"""
def draw_lines(ax, all_objects):
    for index, row in enumerate(all_objects.itertuples()):
        if index > 0:
            prev_row = all_objects.iloc[index-1]
            x = prev_row['latitude']
            y = prev_row['longitude']
            dx = getattr(row, 'latitude') - x
            dy = getattr(row, 'longitude') - y

            ax.arrow(x=x, y=y, dx=dx, dy=dy)

"""
This method will take all points of the map and draw all of them with different colors for different node types
"""
def draw_points(fig, ax, all_objects, ordered_object):
    size = len(all_objects)

    for index, row in enumerate(all_objects.itertuples()):
        if getattr(row, 'type') == 'waste':
            if index == 0:
                scatterStart = ax.scatter(getattr(row, 'latitude'), getattr(row, 'longitude'), color='gold', s=100)
            else:
                scatter1 = ax.scatter(getattr(row, 'latitude'), getattr(row, 'longitude'), color='brown', s=20)
        elif getattr(row, 'type') == 'local_sorting_facility':
            scatter2 = ax.scatter(getattr(row, 'latitude'), getattr(row, 'longitude'), color='red', s=20)
        elif getattr(row, 'type') == 'regional_sorting_facility':
            scatter3 = ax.scatter(getattr(row, 'latitude'), getattr(row, 'longitude'), color='blue', s=20)
        elif getattr(row, 'type') == 'regional_recycling_facility':
            if index == ordered_object.iloc[-1]["id"]:
                scatterEnd = ax.scatter(getattr(row, 'latitude'), getattr(row, 'longitude'), color='pink', s=100)
            else:
                scatter4 = ax.scatter(getattr(row, 'latitude'), getattr(row, 'longitude'), color='green', s=20)

    # A legend is used to make it easier for users to understand the map
    fig.legend((scatter1, scatter2, scatter3, scatter4, scatterStart, scatterEnd), ('waste', 'local_sorting_facility', 'regional_sorting_facility', 'regional_recycling_facility', 'Start', 'End'))

"""
When the upload button is pressed, we ask the user to load in the CSV file
"""
def uploadAction(event=None):
    A = int(scale_value)/100
    B = 1-A

    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    if filename != "":
        all_objects = pd.read_csv(filename,
                                  names=['id', 'longitude', 'latitude', 'type', 'mass', 'risk'])

        # The ordered list of nodes of the path that we want to proceed in to limit pollution
        orderedNodes = waste_distance.get_processing(A, B, all_objects)

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])

        # The ordered nodes are converted back into a Dataframe to help converting to csv
        temp = pd.DataFrame(orderedNodes)

        # Create CSV data file
        temp.to_csv(filename[:len(filename) - 4] + '_Kirby_output.csv', header=False)

        # The figure has the points and the lines drawn on it
        if len(all_objects) < 1500:
            draw_points(fig, ax, all_objects, temp)
            draw_lines(ax, temp)



        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)




# the main Tkinter window
window = Tk()

# setting the title 
window.title('Plastic Distribution')

# dimensions of the main window
window.geometry("1000x1000")

def slider_changed(val):
    global scale_value
    scale_value = val

slider = Scale(
    master=window,
    from_=0,
    to=100,
    orient='horizontal',
    variable=scale_value,
    command=slider_changed,
    label='A'
)
slider.set(50)
slider.pack(pady=30)

button = Button(master=window,
                 command=uploadAction,
                 height=2,
                 width=10,
                 text="Upload CSV")
button.pack()

# run the gui
window.mainloop()