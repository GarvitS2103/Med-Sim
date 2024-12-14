import pyvista as pv
from tkinter import filedialog, messagebox, Tk, Label, Button, OptionMenu, StringVar
import threading
import os

class SurgicalSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hyper-Realistic 3D Surgical Simulation")

        # Create a variable to store the selected body part
        self.selected_body_part = StringVar(root)
        self.selected_body_part.set("Select Body Part")  # default value

        # List of body parts for dropdown menu
        self.body_parts = ["Heart", "Foot", "Lungs"]

        # Create GUI elements
        Label(root, text="Choose a Body Part").pack(pady=10)

        # Dropdown menu to select the body part
        self.body_part_menu = OptionMenu(root, self.selected_body_part, *self.body_parts)
        self.body_part_menu.pack(pady=10)

        Label(root, text="Load a High-Detail 3D Model").pack(pady=10)

        # Button to upload 3D Model
        Button(root, text="Upload 3D Model", command=self.upload_and_load_model).pack(pady=20)

        # Button to exit the application
        Button(root, text="Exit", command=root.quit).pack(pady=10)

    def load_high_detail_model(self, file_path):
        """Load and display a hyper-realistic 3D model."""
        try:
            # Load the STL or OBJ file
            mesh = pv.read(file_path)
            plotter = pv.Plotter()

            plotter.add_mesh(mesh, color='white', show_edges=True)
            plotter.add_text("High-Detail 3D Model", position='upper_left', font_size=12)

            # Run the plotter in a non-blocking way
            threading.Thread(target=self.show_model, args=(plotter,), daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model: {e}")

    def show_model(self, plotter):
        """Display the 3D model in the plotter asynchronously."""
        plotter.view_xy()
        plotter.show()

    def upload_and_load_model(self):
        """Prompt the user to upload a file and load it based on selected body part."""
        body_part = self.selected_body_part.get()
        
        if body_part == "Select Body Part":
            messagebox.showerror("Error", "Please select a body part first.")
            return
        
        # Define directory paths based on the body part selection
        body_part_directory = {
            "Heart": "C:/path_to_heart_models",  # Replace with actual path
            "Foot": "C:/path_to_foot_models",    # Replace with actual path
            "Lungs": "C:/path_to_lungs_models",  # Replace with actual path
        }

        # Get the correct directory for the selected body part
        directory = body_part_directory.get(body_part)

        # Open file dialog to select a file from the selected directory
        if directory and os.path.exists(directory):
            file_path = filedialog.askopenfilename(initialdir=directory, title="Select a 3D Model", filetypes=[("3D Files", "*.stl;*.obj")])
            if file_path:
                self.load_high_detail_model(file_path)
        else:
            messagebox.showerror("Error", f"Directory for {body_part} models not found.")

# Create and run the GUI
root = Tk()
app = SurgicalSimulationApp(root)
root.mainloop()
