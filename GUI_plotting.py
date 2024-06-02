import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Database credentials
DB_NAME = 'AI_scholarly_articles_number_per_year'
DB_USER = 'postgres'
DB_PASS = 'Begemotik'
DB_HOST = 'localhost'

# Function to query the database and plot the data
def plot_data():
    try:
        start_year = int(start_year_entry.get())
        end_year = int(end_year_entry.get())
        selected_topics = [topic for topic in topics if topic_var[topic].get() == 1]

        if not selected_topics:
            messagebox.showwarning("Input Error", "Please select at least one topic.")
            return

        # Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()

        # Query to fetch data
        query = f"""
        SELECT year, topic, count FROM articles
        WHERE year BETWEEN {start_year} AND {end_year} AND topic IN %s;
        """
        cur.execute(query, (tuple(selected_topics),))
        data = cur.fetchall()
        cur.close()
        conn.close()

        # Convert the data to a DataFrame
        df = pd.DataFrame(data, columns=['year', 'topic', 'count'])

        # Plot the data
        plt.figure(figsize=(10, 6))
        for topic in selected_topics:
            topic_data = df[df['topic'] == topic]
            plt.plot(topic_data['year'], topic_data['count'], label=topic)
        
        plt.xlabel('Year')
        plt.ylabel('Number of Articles')
        plt.title('Number of Articles per Year by Topic')
        plt.legend()
        plt.grid(True)
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main application window
root = tk.Tk()
root.title("AI Scholar Articles Analysis")

# Time span input
tk.Label(root, text="Start Year:").grid(row=0, column=0, padx=10, pady=10)
start_year_entry = tk.Entry(root)
start_year_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="End Year:").grid(row=1, column=0, padx=10, pady=10)
end_year_entry = tk.Entry(root)
end_year_entry.grid(row=1, column=1, padx=10, pady=10)

# Topic selection
tk.Label(root, text="Select Topics:").grid(row=2, column=0, padx=10, pady=10)
topics = ["Generative AI", "Natural Language Processing (NLP)", "Reinforcement Learning", "Computer Vision", "AI Ethics and Explainability"]
topic_var = {topic: tk.IntVar() for topic in topics}
for i, topic in enumerate(topics):
    ttk.Checkbutton(root, text=topic, variable=topic_var[topic]).grid(row=3+i, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

# Plot button
plot_button = ttk.Button(root, text="Plot Data", command=plot_data)
plot_button.grid(row=3+len(topics), column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()
