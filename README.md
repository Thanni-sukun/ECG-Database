############# Creating Server and Connect to Database #########
1. Run the code : create_database.py to create database.
2. Run the code : telemetry_server.py to run the server, to connect database to server, to transmit ECG data to server and store in database.

############ Plotting the graph ###############################
1. Run the code: export_to_csv.py to export ECG data from database to csv.
2. Take the file name what have exported to the plot_hex.py or plot_voltage.py.
3. Run the code : plot_hex.py or plot_voltage.py to view the ECG signal graph.

########### Compate ECG Data from software with ECG Data in database #####
1. Run the code: compare_data_v2.py to plot the graph of comparation and see the MSE results.
