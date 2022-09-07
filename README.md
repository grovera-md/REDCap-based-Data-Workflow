# REDCap-based-Data-Workflow

## Instructions

1. Create a new REDCap project, importing the provided xml template ("redcap_template.xml")

2. Enable the REDCap API, and update the REDCap API url and token in the "generate_redcap_data.py " and "redcap_to_sqlite.py " files.

Note: before continuing with the next steps, please verify that all the required dependencies are correctly installed in your system (see import statements of each file)

3. Run the "generate_redcap_data.py" script to upload dummy data on REDCap

4. Run the "initialize_sqlite_db.py" script to initialize the local sqlite database

5. Run the "redcap_to_sqlite.py" script to retrieve data from the REDCap API and store them in the local sqlite database

6. Run the "plot_results.py" script to query the sqlite database, compute new data and plot results.

To evaluate the performance (execution time) of the first two steps fo the process (REDCap API data export, SQLite data import), execute the script "test_01.py"; for SQLite database query, refer to the "test_02.py" file.
