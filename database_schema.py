# Description: This script creates the database schema for the movies database.
# Note:create a database named movies before running the file
import mysql.connector

# Establish connection to MySQL server
conn=mysql.connector.connect(host="localhost",user="root",password="",database="movies")
# Create cursor object
cursor = conn.cursor()

# Create tables
#Schema for Movie table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Movie (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    year_of_release INT,
    average_rating DECIMAL(3, 2)
)
""")
#Schema for Genre table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Genre (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
)
""")
#Schema for Actor table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Actor (
    actor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
)
""")
#Schema for Technician table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Technician (
    technician_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
)
""")
#Schema for MovieGenre table it is a many to many relationship between Movie and Genre
cursor.execute("""
CREATE TABLE IF NOT EXISTS MovieGenre (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY(movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
)
""")
#Schema for MovieActor table it is a many to many relationship between Movie and Actor
cursor.execute("""
CREATE TABLE IF NOT EXISTS MovieActor (
    movie_id INT,
    actor_id INT,
    PRIMARY KEY(movie_id, actor_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (actor_id) REFERENCES Actor(actor_id)
)
""")
#Schema for MovieTechnician table it is a many to many relationship between Movie and Technician
cursor.execute("""
CREATE TABLE IF NOT EXISTS MovieTechnician (
    movie_id INT,
    technician_id INT,
    PRIMARY KEY(movie_id, technician_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (technician_id) REFERENCES Technician(technician_id)
)
""")
#Schema for UserRating table
cursor.execute("""
CREATE TABLE IF NOT EXISTS UserRating (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    rating INT,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
)
""")

# Commit changes and close cursor and connection
conn.commit()
cursor.close()
conn.close()
