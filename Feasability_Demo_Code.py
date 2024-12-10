import tkinter as tk
from tkinter import simpledialog
from datetime import datetime, timedelta
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar

#import custom funcitons (Not being used for demo)
import Date_to_functions

class Timeline(tk.Tk):

    #this func creates items of the GUI before rendering the timeline. Addtionally it fills up a list to subsitute for the lack of
    #data extraction from actual test files.
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)  #allows the column to expand
        self.title('Forensics Timeline')
        self.iconbitmap(r'forensic.ico')

        self.geometry('800x600')  #sets a default window size
        self.minsize(800, 600) #minimum size allowed

        self.rowconfigure(0, weight=1, minsize=int(self.winfo_screenheight()*0.10))
        self.rowconfigure(1, weight=1, minsize=int(self.winfo_screenheight()*0.90))
        #self.rowconfigure(1, weight=1, minsize=int(self.winfo_screenheight()*0.20))

        #create a top frame instance for buttons
        self.top_frame = tk.Canvas(self, bg="lightgray")
        self.top_frame.grid(row=0, column=0, sticky='nsew')

        #create title for application
        title_label = tk.Label(self.top_frame, text="Forensic Timeline", font=('Arial', 20, 'bold'), bg='lightgray')
        title_label.pack(side="top", padx=10)
        
        #creates the canvas and allow it to expand, on the bottom row
        self.timeline_canvas = tk.Canvas(self, bg='lightgray')
        self.timeline_canvas.grid(row=1, column=0, sticky='nsew')

        #creates filter buttons
        self.filter_button = tk.Button(self.top_frame, text="Filter Dates", command=self.open_filter_window)
        self.filter_button.pack(side="left", padx=10)

        #creates a label to display current filter date
        self.current_filter_label = tk.Label(self.top_frame, text="N/A", font=('Arial', 14), bg="lightgray")
        self.current_filter_label.pack(side="left")

        #creates an instance of a button to clear the filter
        self.clear_filter_button = tk.Button(self.top_frame, text="Clear Filter", command=self.clear_filter)
        self.clear_filter_button.pack(side="left", padx=10)

        #Initialize filter dates
        self.filter_start = None
        self.filter_end = None

        # Timeline events - Fake data for the demo
        self.timeline_list = [
            (datetime(2012, 1, 5, 10, 15), "Incident 1: Unauthorized access attempt detected."),
            (datetime(2012, 4, 18, 14, 45), "Incident 2: Malware detected on workstation."),
            (datetime(2013, 6, 30, 9, 30), "Incident 3: Suspicious file upload flagged."),
            (datetime(2013, 11, 10, 16, 0), "Incident 4: Password breach on user account."),
            (datetime(2014, 2, 5, 11, 20), "Incident 5: Network traffic spike detected."),
            (datetime(2014, 9, 25, 19, 10), "Incident 6: Phishing attempt via email."),
            (datetime(2015, 3, 12, 8, 45), "Incident 7: Unauthorized use of credentials."),
            (datetime(2015, 7, 17, 22, 15), "Incident 8: Suspicious network scan detected."),
            (datetime(2016, 1, 4, 14, 20), "Incident 9: New exploit detected on server."),
            (datetime(2016, 5, 18, 10, 5), "Incident 10: Unusual login time flagged."),
            (datetime(2017, 8, 30, 17, 25), "Incident 11: Firewall rules modified without approval."),
            (datetime(2017, 12, 14, 9, 50), "Incident 12: Unauthorized admin access attempt."),
            (datetime(2018, 3, 7, 12, 15), "Incident 13: Sensitive data accessed without permission."),
            (datetime(2018, 11, 20, 16, 45), "Incident 14: VPN credentials used from unknown IP."),
            (datetime(2019, 1, 30, 11, 35), "Incident 15: Suspicious file transfer on server."),
            (datetime(2019, 4, 22, 13, 0), "Incident 16: Insider threat detected through system audit."),
            (datetime(2019, 9, 5, 18, 50), "Incident 17: Malware removed after incident report."),
            (datetime(2020, 2, 10, 7, 30), "Incident 18: Multiple failed login attempts."),
            (datetime(2020, 5, 18, 20, 10), "Incident 19: Unauthorized access to network resources."),
            (datetime(2020, 10, 8, 15, 45), "Incident 20: Security patch applied after breach."),
            (datetime(2021, 3, 14, 14, 25), "Incident 21: Failed brute-force attack."),
            (datetime(2021, 7, 12, 9, 15), "Incident 22: Suspicious activity on admin account."),
            (datetime(2022, 1, 23, 11, 50), "Incident 23: New malware detected in email attachments."),
            (datetime(2022, 5, 28, 16, 35), "Incident 24: Social engineering attack reported."),
            (datetime(2022, 9, 11, 19, 10), "Incident 25: Security anomaly during routine audit."),
            (datetime(2023, 1, 1, 9, 0), "Incident 26: Unusual data transfer flagged."),
            (datetime(2023, 1, 5, 11, 30), "Incident 27: Ransomware detected on multiple systems."),
            (datetime(2023, 1, 10, 15, 45), "Incident 28: Unauthorized software installation."),
            (datetime(2023, 1, 15, 13, 0), "Incident 29: Phishing attack reported."),
            (datetime(2023, 1, 20, 14, 0), "Incident 30: Unauthorized network access detected."),
            (datetime(2023, 1, 25, 16, 15), "Incident 31: Malicious insider activity identified."),
            (datetime(2023, 1, 30, 10, 0), "Incident 32: Security patch applied after malware incident."),
            (datetime(2023, 2, 2, 11, 0), "Incident 33: Suspicious file downloads detected."),
            (datetime(2023, 2, 5, 18, 30), "Incident 34: Data exfiltration attempt blocked."),
            (datetime(2023, 2, 10, 12, 15), "Incident 35: Compromised credentials reported."),
            (datetime(2023, 2, 15, 14, 30), "Incident 36: Unusual login locations identified."),
            (datetime(2023, 2, 20, 9, 30), "Incident 37: Malware analysis initiated."),
            (datetime(2023, 2, 25, 16, 0), "Incident 38: Unauthorized device connected to network."),
            (datetime(2023, 3, 2, 13, 15), "Incident 39: Keylogger detected on workstation."),
            (datetime(2023, 3, 5, 10, 0), "Incident 40: Data leak reported."),
            (datetime(2023, 4, 22, 13, 0), "Incident 41: Insider threat detected through system audit."),
            (datetime(2023, 9, 5, 18, 50), "Incident 42: Malware removed after incident report."),
            (datetime(2024, 2, 10, 7, 30), "Incident 43: Multiple failed login attempts."),
            (datetime(2024, 5, 18, 20, 10), "Incident 44: Unauthorized access to network resources."),
            (datetime(2024, 10, 8, 15, 45), "Incident 45: Security patch applied after breach."),
            (datetime(2025, 3, 14, 14, 25), "Incident 46: Failed brute-force attack."),
            (datetime(2025, 7, 12, 9, 15), "Incident 47: Suspicious activity on admin account."),
            (datetime(2026, 1, 23, 11, 50), "Incident 48: New malware detected in email attachments."),
            (datetime(2026, 5, 28, 16, 35), "Incident 49: Social engineering attack reported."),
            (datetime(2026, 9, 11, 19, 10), "Incident 50: Security anomaly during routine audit.")
        ]

        #create a function to zoom in and out of the current timline
        self.timeline_canvas.bind("<MouseWheel>", self.zoom_in_out)

        #bind the configure event to adjust the canvas after each mousewheel movement
        self.timeline_canvas.bind("<Configure>", self.append_canvas)

    #this func is responsible for for taking the mousewheel input and detemrining wheather to render the canvas zoomed in or out
    def zoom_in_out(self, event):
        #zoom in/out the timeline based on mouse wheel movement and mouse position.
        if not self.timeline_list or len(self.timeline_list) < 2:
            return  #if less than two events then return as you should not need to zoom in further when only two events remain

        #ensure filter_start and filter_end are inistialzed
        if self.filter_start is None or self.filter_end is None:
            #initialize to the full range of the timeline if no filter is set
            filtered_list = [dt for dt, _ in self.timeline_list]
            filtered_list.sort()
            self.filter_start = filtered_list[0]
            self.filter_end = filtered_list[-1]

        #get mouse x position on the canvas (Further investigating)
        mouse_x = self.timeline_canvas.canvasx(event.x)
        canvas_width = self.timeline_canvas.winfo_width() - 250  #change for padding on both sides
        effective_width = canvas_width - 250 #padding of 125 pixels on both sides
     
        #filtered dates
        filtered_list = [dt for dt, _ in self.timeline_list]
        filtered_list.sort()
        first_datetime = filtered_list[0]
        last_datetime = filtered_list[-1]

        #calculate total seconds for the current timeline range
        total_seconds = (last_datetime - first_datetime).total_seconds()
        
        #determine the amount to adjust based on mouse position (for example far left means only take time away from filter_end)
        adjustment_seconds = total_seconds * 0.01 #(can adjust to set how much it zooms in/out by based on each mousewheel scroll)
        new_start = self.filter_start
        new_end = self.filter_end

        #calculate section boundaries to determine how much to add or minus from start and end date
        section_width = effective_width / 5
        section_boundaries = [i * section_width for i in range(1, 6)]  #5 sections boundaries in total

        #adjust filters based on mouse position
        if mouse_x < section_boundaries[0]:  #first section (minus/add seconds from end/start filter)
            if event.delta > 0:  #Zoom in
                new_end -= timedelta(seconds=adjustment_seconds)  #shrink to filter
            else:  #Zoom out
                new_end += timedelta(seconds=adjustment_seconds)  #expand to filter

        elif mouse_x < section_boundaries[1]:  #second section
            if event.delta > 0:  #Zoom in
                new_start += timedelta(seconds=adjustment_seconds / 6)  #slightly shrink from start filter
                new_end -= timedelta(seconds=adjustment_seconds * 5 / 6)  #shrink to end filter more
            else:  #Zoom out
                new_start -= timedelta(seconds=adjustment_seconds / 6)  #expand from start filter slightly
                new_end += timedelta(seconds=adjustment_seconds * 5 / 6)  #expand to end filter more

        elif mouse_x < section_boundaries[2]:  #third section (Middle)
            if event.delta > 0:  #Zoom in
                new_start += timedelta(seconds=adjustment_seconds / 2)  #shrink from start filter
                new_end -= timedelta(seconds=adjustment_seconds / 2)  #shrink to end filter
            else:  #Zoom out
                new_start -= timedelta(seconds=adjustment_seconds / 2)  #expand from start filter
                new_end += timedelta(seconds=adjustment_seconds / 2)  #expand to end filter

        elif mouse_x < section_boundaries[3]:  #fourth section
            if event.delta > 0:  #Zoom in
                new_start += timedelta(seconds=adjustment_seconds * 5 / 6)  #shrink from start filter more
                new_end -= timedelta(seconds=adjustment_seconds / 6)  #shrink to end filter slightly
            else:  #Zoom out
                new_start -= timedelta(seconds=adjustment_seconds * 5 / 6)  #expand from start filter more
                new_end += timedelta(seconds=adjustment_seconds / 6)  #expand to end filter slightly

        else:  #fifth section
            if event.delta > 0:  #Zoom in
                new_start += timedelta(seconds=adjustment_seconds)  #shrink from filter
            else:  #Zoom out
                new_start -= timedelta(seconds=adjustment_seconds)  #expand from filter

        #check number of events after any adjustments
        def count_events(start, end):
            return len([dt for dt in filtered_list if start <= dt <= end])

        #If zooming out, ensure its not allowed to zoom out more than two events or exceed the overall range
        if event.delta < 0:
            while True:
                event_count = count_events(new_start, new_end)
                #prevent going over what is held in the data structure
                if event_count <= 3 or new_start < first_datetime or new_end > last_datetime:
                    break
                new_start -= timedelta(seconds=adjustment_seconds)
                new_end += timedelta(seconds=adjustment_seconds)
        else:
            #prevent zooming in if it leaves 3 events or fewer
            event_count_after_zoom = count_events(new_start, new_end)
            if event_count_after_zoom <= 3:
                return  #do not apply the zoom in new timeline

        #ensure new start and end do not exceed the overall date range
        new_start = max(new_start, first_datetime)
        new_end = min(new_end, last_datetime)

        #update filter start and end
        self.filter_start = new_start
        self.filter_end = new_end

        #update the filter labels to reflect the new range
        self.current_filter_label.config(text=f"{self.filter_start.strftime('%Y:%m:%d')} : {self.filter_end.strftime('%Y:%m:%d')}")

        #redraw the canvas with the new filters by calling the render function
        self.append_canvas()

    #this func is used to open a window to allow the user to select a custom date range.
    def open_filter_window(self):
        #open a new window with calendars to select the date range for filtering.
        top = tk.Toplevel(self)
        #name the new window as the below title
        top.title("Filter Dates")

        #create the two caldener boxed to select dates for both the start and end filters
        tk.Label(top, text="From Date:").grid(row=0, column=0, padx=10, pady=10)
        from_calendar = Calendar(top, selectmode='day')
        from_calendar.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(top, text="To Date:").grid(row=1, column=0, padx=10, pady=10)
        to_calendar = Calendar(top, selectmode='day')
        to_calendar.grid(row=1, column=1, padx=10, pady=10)

        #func to take selected dates and set the filters before re-rendering the timeline
        def apply_filter():

            #apply the selected date range filter and close the window.
            try:
                self.filter_start = from_calendar.selection_get()
                self.filter_end = to_calendar.selection_get()

                if self.filter_start and self.filter_end:
                    self.filter_start = datetime.combine(self.filter_start, datetime.min.time())
                    self.filter_end = datetime.combine(self.filter_end, datetime.max.time())

                    if self.filter_start > self.filter_end:
                        messagebox.showerror("Error", "From date must be before To date.")
                        return
                    
                    #update the current filter label with selected dates to improve clarity
                    self.current_filter_label.config(text=f"{self.filter_start.strftime('%Y-%m-%d')} - {self.filter_end.strftime('%Y-%m-%d')}")

                self.append_canvas()
                #destroy top window with filter box
                top.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        #button which applys the filters when pressed
        tk.Button(top, text="Apply Filter", command=apply_filter).grid(row=2, column=0, columnspan=2, pady=10)

    def clear_filter(self):
        #clear the date filter and show all incidents.
        self.filter_start = None
        self.filter_end = None
        self.current_filter_label.config(text="N/A")  #changes the filter label to N/A

        self.append_canvas()

    def append_canvas(self, event=None):
        #update the canvas with timeline representation of the datetime events.
        self.timeline_canvas.delete('all')  #clears the previous render

        #get the canvas width and height
        current_width = self.timeline_canvas.winfo_width()
        current_height = self.timeline_canvas.winfo_height()

        #Initialize line size based on the current width
        if current_width > 0:
            self.line_size = current_width - 250  #use current width and minus padding

        vertical_position = current_height / 4  #center the timeline

        #prepare filtered timeline data
        if self.filter_start and self.filter_end:
            filtered_timeline = [
                (dt, notes) for dt, notes in self.timeline_list
                if self.filter_start <= dt <= self.filter_end
            ]
        else:
            filtered_timeline = self.timeline_list  #show all incidents if no filter

        #sort the filtered timeline
        filtered_timeline.sort(key=lambda x: x[0])

        if not filtered_timeline:  #if no incidents match the filter
            messagebox.showinfo("Filter Result", "No incidents found in this date range.")
            return

        #get total seconds
        first_datetime = filtered_timeline[0][0]
        last_datetime = filtered_timeline[-1][0]
        total_seconds = (last_datetime - first_datetime).total_seconds()

        #initialize variables to track incidents in segments / based on current timescale.
        num_segments = 30  #changable

        
        segment_size = self.line_size / num_segments
        incident_count_per_segment = [0] * num_segments
        incidents_in_segment = [[] for _ in range(num_segments)]  #store incidents per segment

        #count incidents in each segment
        for dt, notes in filtered_timeline:
            x = (dt - first_datetime).total_seconds() / total_seconds * self.line_size if total_seconds > 0 else 0
            segment_index = min(int(x // segment_size), num_segments - 1)
            incident_count_per_segment[segment_index] += 1
            incidents_in_segment[segment_index].append((dt, notes))  #store incident details

        #draw the timeline segments
        for i in range(num_segments):
            x_start = 50 + i * segment_size
            x_end = 50 + (i + 1) * segment_size
            incident_count = incident_count_per_segment[i]

            #determine color based on how many incidents occur in the segment
            color = self.get_heatmap_colour(incident_count)
            self.timeline_canvas.create_rectangle(x_start, vertical_position - 10, x_end, vertical_position + 10, fill=color, outline=color)

        #labels for start and end dates
        self.timeline_canvas.create_text(30, vertical_position, text=first_datetime.strftime('%Y-%m-%d %H:%M'), anchor='e')
        self.timeline_canvas.create_text(50 + self.line_size + 20, vertical_position, text=last_datetime.strftime('%Y-%m-%d %H:%M'), anchor='w')

        #staggering configurations with padding to be reset after every 5 incidents
        label_offset = 20  #vertical padding for staggered labels
        vertical_spacing = 45  #spacing between labels
        vertical_position_offset = 10  #offset for labels to appear above/below
        base_padding = 25  #reset padding after every 5 incidents
        incident_counter = 0  #track incident for padding reset

        #process each segment for drawing incidents
        for i in range(num_segments):
            incidents = incidents_in_segment[i]  #get incidents for the current segment
            incident_count = len(incidents)  #count of incidents in this segment

            if incident_count <= 3:  #less than or equal to 4 incidents - show individual incidents
                for index, (dt, notes) in enumerate(incidents):
                    #calculate the position based on the timeline
                    x = (dt - first_datetime).total_seconds() / total_seconds * self.line_size if total_seconds > 0 else 0

                    #reset padding after every 5(default) incidents
                    if incident_counter == 6:
                        incident_counter = 0  # Reset counter
                        base_padding = 25  # Reset padding after 5 incidents

                    #determine whether to stagger above or below the timeline
                    if incident_counter % 2 == 0:  #even position: label above
                        base_y = vertical_position - vertical_position_offset - (incident_counter * vertical_spacing) - base_padding
                        label_anchor = 's'  #label anchor for below the timeline
                    else:  #odd position: label below
                        base_y = vertical_position + vertical_position_offset + (incident_counter * vertical_spacing) + base_padding
                        label_anchor = 'n'  #label anchor for above the timeline

                    #create vertical line from label to timeline
                    self.timeline_canvas.create_line(50 + x, base_y + 20, 50 + x, vertical_position, fill='blue', dash=(2, 2))

                    #create a dot on the timeline to represent the event
                    dot_radius = 2  # Radius of the dot
                    self.timeline_canvas.create_oval(
                        50 + x - dot_radius, vertical_position - dot_radius,
                        50 + x + dot_radius, vertical_position + dot_radius,
                        fill='red', outline='red'
                    )

                    #create date label for incidents
                    date_time_label = tk.Label(self.timeline_canvas, text=dt.strftime('%Y-%m-%d\n%H:%M'), bg='white', cursor="hand2")
                    
                    #bind the left mouse click to the function that shows incident details
                    date_time_label.bind("<Button-1>", lambda event, d=dt, n=notes: self.show_incident_details(d, n))

                    #create the label in the canvas
                    self.timeline_canvas.create_window((50 + x, base_y + label_offset), window=date_time_label, anchor=label_anchor)

                    incident_counter += 1  #increment counter for padding reset

            else:  #more than 4 incidents - group into a single mark
                start_date = incidents[0][0]  #first incident date
                end_date = incidents[-1][0]  #last incident date
                
                #create cluster label with vertical padding
                cluster_label_text = (
                    f"{start_date.strftime('%Y-%m-%d')}\n"
                    f"{end_date.strftime('%Y-%m-%d')}"
                )
                cluster_x = (start_date - first_datetime).total_seconds() / total_seconds * self.line_size if total_seconds > 0 else 0
                
                #reset padding after every 5 incidents
                if incident_counter == 6:
                    incident_counter = 0  #reset counter
                    base_padding = 25  #reset padding after 5 incidents

                #determine staggering for cluster labels
                if incident_counter % 2 == 0:
                    #stagger above
                    base_y = vertical_position - vertical_position_offset - base_padding
                    label_anchor = 's'  # Label anchor for below the timeline
                else:
                    #stagger below
                    base_y = vertical_position + vertical_position_offset + base_padding
                    label_anchor = 'n'  #label anchor for above the timeline

                #create cluster label (tk.Label) with a white background
                cluster_label = tk.Label(self.timeline_canvas, text=cluster_label_text, bg='white', cursor="hand2")

                #bind click event to show details of all incidents in the cluster
                cluster_label.bind(
                    "<Button-1>",
                    lambda event, segment_incidents=incidents: self.show_cluster_details(segment_incidents)
                )

                #create the label in the canvas
                self.timeline_canvas.create_window((50 + cluster_x, base_y + label_offset), window=cluster_label, anchor=label_anchor)

                #draw vertical line from the cluster dot to the label
                self.timeline_canvas.create_line(50 + cluster_x, vertical_position, 50 + cluster_x, base_y + 20, fill='blue', dash=(2, 2))

                #draw the cluster as a single mark
                dot_radius = 4  #radius of the dot for cluster
                self.timeline_canvas.create_oval(
                    50 + cluster_x - dot_radius, vertical_position - dot_radius,
                    50 + cluster_x + dot_radius, vertical_position + dot_radius,
                    fill='blue', outline='blue'
                )

                incident_counter += 1  #increment counter for padding reset
        
        #update the scroll region
        self.timeline_canvas.config(scrollregion=self.timeline_canvas.bbox("all"))

    def show_cluster_details(self, incidents):
        """Display details for the incidents in a cluster in a new window."""
        cluster_window = tk.Toplevel(self)
        cluster_window.title("Cluster Incident Details")

        #add a text widget to display the details
        details_text = tk.Text(cluster_window, wrap='word', height=20, width=50)
        details_text.pack(expand=True, fill='both')

        #loop through incidents and append details to the text widget
        for dt, notes in incidents:
            details_text.insert(tk.END, f"Date: {dt.strftime('%Y-%m-%d %H:%M')}\nDetails: {notes}\n\n")

        details_text.config(state=tk.DISABLED)  #disable editing of the text
        tk.Button(cluster_window, text="Close", command=cluster_window.destroy).pack(pady=10)


    def show_incident_details(self, dt, notes):
        """Show incident details in a new window."""
        detail_window = tk.Toplevel(self)  #create a new top-level window
        detail_window.title("Incident Details")

        #create labels for date and notes
        tk.Label(detail_window, text=f"Date: {dt.strftime('%Y-%m-%d %H:%M')}", font=('Arial', 12)).pack(pady=10)
        tk.Label(detail_window, text=f"Notes: {notes}", wraplength=300, justify="left").pack(pady=10)

        #add a close button
        tk.Button(detail_window, text="Close", command=detail_window.destroy).pack(pady=10)


    def get_heatmap_colour(self, count):
        """Determine color based on incident count."""
        #define color stops for incident counts 0, 1, 2, 4, 6, 10, 12+
        if count == 0:
            return '#99FF33'  #Light Green (no incidents)
        elif count == 1:
            return '#00FF00'  #Green
        elif count == 2:
            return '#FFFF00'  #Yellow
        elif count == 4:
            return '#FFCC00'  #Orange yellow
        elif count == 6:
            return '#FF9900'  #Orange
        elif count == 10:
            return '#FF6600'  #Deep orange
        elif count >= 12:
            return '#FF0000'  #Red (high density)

        #return a default color if the count doesn't match exact stops
        return '#33FF33'  #default green for other numbers


#run everything in main loop
if __name__ == "__main__":
    app = Timeline()
    app.mainloop()
