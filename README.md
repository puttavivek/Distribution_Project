Distribution Project
====================

This project helps solve routing problems for a specific location by generating data files that can be used with AMPL, running the AMPL model, and visualizing the solution on a map.

Getting Started
---------------

Follow the steps below to run the project:

### 1\. Generate Data Files

First, run the location\_to\_ampl.py script. This script will generate the necessary data files for your location.

#### Inputs:

*   **Location:** Enter the location name (e.g., "Fairview, Halifax, Nova Scotia, Canada") that you want to solve the problem for.
    
*   **Directory:** Provide the directory where the files should be saved (e.g., "C:/Users/YourName/Path/").
    
*   **City Name:** Enter the name of the city or location to save the graph files under (e.g., "fairview").
    

#### Outputs:

*   **Excel File:** Contains the location data.
    
*   **Updated Excel and Text Files:** These files include data that can be directly used in AMPL.
    

### 2\. Run the AMPL Model

After generating the data files, use them to run your AMPL model. Save the solution of the route in the graph\_output.txt file.

### 3\. Visualize the Route

Once you have the solution, run the map.py script to visualize the route on a map.

This script will update the route\_map.html file, which you can then open in your browser to view the route.

Summary
-------

1.  Run location\_to\_ampl.py to generate data files.
    
2.  Use the generated data to run your AMPL model.
    
3.  Run map.py to visualize the solution.
    

Feel free to reach out if you encounter any issues or have questions about the project.
