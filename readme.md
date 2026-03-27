# SPyC: Simple Automated Statistical Process Control System
## Video Demo: [https://youtu.be/PxtqLKx8Gp0](https://youtu.be/PxtqLKx8Gp0)

## Background: 

Statistical Process Control or SPC is an approach to maintain consistent quality of a process by understanding its underlying variation and applying a set of rules to the data, which allow us to distinguish meaningful patterns (e.g., signal) in the underlying data from typical "normal" variation (e.g., noise).  By understanding the nature of the underlying variation, we can make informed decisions about when we might need to take action on a process (e.g., make a fix), and perhaps more importantly, when to leave the process alone. 

The main idea behind SPC is simple: based on a normal distribution most data should follow certain "rules" due to the fact that certain sequences of points are simply unlikely due to random chance alone.  For example, it is unlikely (albiet not impossible) for a data point to occur more than 3 standard deviations from the mean, which would indicate the point should be investigated.  There are 8+ different "rules" which are often applied to data to identify such signals.  SPyC contains implementations for 4 of the most common patterns used in industry.    

For a more complete description of SPC: https://en.wikipedia.org/wiki/Statistical_process_control

## Motivation 

While the underlying math/statistics are relatively simple, there are many practical challenges in deploying SPC in the "real world". 

1. **Time**: Processes and rules must be applied in real-time to be useful.
2. **Work**: Organizations have 100's or 1000's of processes that must all be monitored - an impossible task to perform manually.  
3. **Data**: It's desirable to have a single source of truth 
4. **Management**: When we investigate or make a change, how is it documented?  How are we performing overall?
5. **Visualization**: Charts should be visually apealing and easy to use. 

## Solution 

SPyC (pronounced "spicy") is a proof-of-concept web-based application designed to begin to address the 5 major challenges outlined above.  SPyC is capable of connecting to an underlying database, generating SPC charts in real-time, serving the charts to a web server, and providing users to add notes and documentation back into the database to maintain tracability between the a decision and the underlying data used to generate that decision. 

SPyC is built on several components: 
- Database: SQLite
- Back-end: Python
- Web Framework: Flask
- Visualization: Plotly.io
- Basic Styling: Bootstrap CSS

## Workflow

SPyC has a few main features that have currently been implemented: 
1. Dashboard: see an overall performance summary of all measurements in the database. 
2. Control charts: visualize each process individually.  All plots are interactive and can be zoomed/expanded as needed. 
3. Engineering View: Add notes, which are tied to specific measurements.  When a note is added, control charts reflect this new status. 

## Files

- `spc.db` :: SQLite database covering all aspects of the back end (data and users). Current tables impleneted include: 
    - users: user ID / hash of password
    - measurements:  actual process data.
    - features: contains data related to specific features measured (e.g., name and specifications).  
    - product: contains data specific to a product which contains features and measurements. 
    - notes: where we document anything related to the actual measurements taken. 

- `app.py` :: Contains the flask code used to generate the web app. 

- `config.py` :: Storage for basic contstants, variables, and sql queries used throughout the app.

- `helpers.py` :: Basic helper functions to make it easier to work between CS50.sql and Pandas libraries. 

- `gendata.py` :: Used to generate sample data to populate database. 

- `spc.py` :: Contains `SPC` class, which provdes all of the logic/math operations used within the app.  The `SPC` class was implemented in python as a `@dataclass`, which provides a simple/pythonic means to implement isolated methods and easily tweak input parameters: 
    - Identification of rule violations
    - Calculation of metrics (e.g., yield)
    - Generation of SPC visualizations.

Attributes of the `SPC` class can be accessed trivially, for example: 
- `SPC.control_chart()`
- `spc.lsl` (spec limits)
- `spc.data` All relevant data combined into a simple pandas dataframe. 

- `\sql` :: Contains general queries and database operations saved as individual `.sql` files.  Since the same queries/operations are performed in multiple areas throughout the apps, it made sense to refactor the queries outside the main app. 

- `\templates` : Contains .html templates used to generate all web pages. 

# Roadmap / Future Improvements: 

There are many additional features, which would make SPyC a more robust and usable production-ready applicaion. 

1. Implement additional control chart SPC rules
2. Additional visualizations (e.g., histograms) for process capability
3. Additional control chart types (e.g., percent defective, sample average)
4. Improved data (input) validation: Ensure users cannot enter notes related to wrong feature. 
5. Data pipeline: Connect `spc.db` to a real production system.  
6. Improve visualization of dashboard / metrics page. 

