from flask import Flask, request, jsonify,render_template,redirect,url_for
import mysql.connector
conn=mysql.connector.connect(host="localhost",user="root",password="",database="movies")
cursor = conn.cursor()
app = Flask(__name__)


@app.route('/')
def index():
    #loading the index page
    return render_template('index.html')


@app.route('/actorregister')
def actorregister():
    #getting the auto increment id from the actor table and passing it to the register.html page to display it in the form
    cursor.execute("SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'movies' AND TABLE_NAME = 'actor'")
    auto_increment_id = cursor.fetchone()[0]
    return render_template('register.html',auto_increment_id=auto_increment_id,api="/addactor")


@app.route('/technicianregister')
def technicianregister():
    #getting the auto increment id from the technician table and passing it to the register.html page to display it in the form
    cursor.execute("SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'movies' AND TABLE_NAME = 'technician'")
    auto_increment_id = cursor.fetchone()[0]
    return render_template('register.html',auto_increment_id=auto_increment_id,api="/addtechnician")


@app.route('/genreregister')
def genreregister():
    #getting the auto increment id from the genre table and passing it to the register.html page to display it in the form
    cursor.execute("SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'movies' AND TABLE_NAME = 'genre'")
    auto_increment_id = cursor.fetchone()[0]
    return render_template('register.html',auto_increment_id=auto_increment_id,api="/addgenre")


@app.route('/addactor',methods=['POST'])
def addactor():
    #Adding the actor details to the actor table using the POST method
    name = request.form['name']
    cursor.execute("INSERT INTO actor (name) VALUES ('{}')".format(name))
    conn.commit()
    return redirect(url_for('actorregister'))


@app.route('/addtechnician',methods=['POST'])
def addtechnician():
    #Adding the technician details to the technician table using the POST method
    name = request.form['name']
    cursor.execute("INSERT INTO technician (name) VALUES ('{}')".format(name))
    conn.commit()
    return redirect(url_for('technicianregister'))


@app.route('/addgenre',methods=['POST'])
def addgenre():
    #Adding the genre details to the genre table using the POST method
    name = request.form['name']
    cursor.execute("INSERT INTO genre (name) VALUES ('{}')".format(name))
    conn.commit()
    return redirect(url_for('genreregister'))


@app.route('/movieregister')
def movieregister():
    #getting the auto increment id from the movie table and passing it to the movieregister.html page to display it in the form and also retrieving the genres,actors and technicians from the respective tables to display in the form
    cursor.execute("SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'movies' AND TABLE_NAME = 'movie'")
    auto_increment_id = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM genre")
    genres=cursor.fetchall()
    cursor.execute("SELECT * FROM actor")
    actors=cursor.fetchall()
    cursor.execute("SELECT * FROM technician")
    technicians=cursor.fetchall()
    return render_template('movieregister.html',auto_increment_id=auto_increment_id,genres=genres,actors=actors,technicians=technicians)


@app.route('/addmovie',methods=['POST'])
def addmovie():
    #Adding the movie details to the movie table using the POST method and also adding the genre,actor and technician details to the respective tables.
    movie_id=request.form['movie_id']
    name = request.form['name']
    year_of_release = request.form['year_of_release']
    average_rating = request.form['average_rating']
    genre_id = request.form['genre_id']
    actor_id = request.form['actor_id']
    technician_id = request.form['technician_id']
    query = "INSERT INTO movie (name,year_of_release,average_rating) VALUES ('{}',{},'{}')".format(name,year_of_release,average_rating)
    cursor.execute(query)
    conn.commit()
    for i in genre_id.split(","):
        query = "INSERT INTO MovieGenre (movie_id,genre_id) VALUES ({},{})".format(int(movie_id),int(i))
        cursor.execute(query)
        conn.commit()
    for i in actor_id.split(","):
        query = "INSERT INTO MovieActor (movie_id,actor_id) VALUES ({},{})".format(int(movie_id),int(i))
        cursor.execute(query)
        conn.commit()
    for i in technician_id.split(","):
        query = "INSERT INTO MovieTechnician (movie_id,technician_id) VALUES ({},{})".format(int(movie_id),int(i))
        cursor.execute(query)
        conn.commit()
    return redirect(url_for('movieregister'))


@app.route('/showmovies')
def showmovies():
    #retrieving the movie details from the movie table and passing it to the moviedashboard.html page to display it,also retrieving the genres,actors and technicians from the respective tables to display in the form used for filtering.
    cursor.execute("SELECT * FROM movie")
    movies=cursor.fetchall()
    cursor.execute("SELECT * FROM genre")
    genres=cursor.fetchall()
    cursor.execute("SELECT * FROM actor")
    actors=cursor.fetchall()
    cursor.execute("SELECT * FROM technician")
    technicians=cursor.fetchall()
    return render_template('moviedashboard.html',movies=movies,tgenres=genres,tactors=actors,ttechnicians=technicians)


@app.route('/showactors')
def showactors():
    #retrieving the actor details from the actor table and passing it to the dashboard.html page to display it. and also retrieving the actors who are not associated with any movie to display in the form used for deleting.
    cursor.execute("SELECT * FROM actor")
    actors=cursor.fetchall()
    cursor.execute("SELECT actor_id FROM actor WHERE actor_id NOT IN (SELECT DISTINCT actor_id FROM movieactor)")
    dactors=cursor.fetchall()
    dactors=[i[0] for i in dactors]
    return render_template('dashboard.html',data=actors,name="Actors",delete_data=dactors)


@app.route('/showtechnicians')
def showtechnicians():
    #retrieving the technician details from the technician table and passing it to the dashboard.html page to display it. and also retrieving the technicians who are not associated with any movie to display in the form used for deleting.
    cursor.execute("SELECT * FROM technician")
    technicians=cursor.fetchall()
    cursor.execute("SELECT technician_id FROM technician WHERE technician_id NOT IN (SELECT DISTINCT technician_id FROM movietechnician)")
    dtechnicians=cursor.fetchall()
    dtechnicians=[i[0] for i in dtechnicians]
    return render_template('dashboard.html',data=technicians,name="Technicians",delete_data=dtechnicians)


@app.route('/showgenres')
def showgenres():
    #retrieving the genre details from the genre table and passing it to the dashboard.html page to display it. and also retrieving the genres which are not associated with any movie to display in the form used for deleting.
    cursor.execute("SELECT * FROM genre")
    genres=cursor.fetchall()
    cursor.execute("SELECT genre_id FROM genre WHERE genre_id NOT IN (SELECT DISTINCT genre_id FROM moviegenre)")
    dgenres=cursor.fetchall()
    dgenres=[i[0] for i in dgenres]
    return render_template('dashboard.html',data=genres,name="Genres",delete_data=dgenres)


@app.route('/moviedetails/<int:movie_id>')
def actors(movie_id):
    #retrieving the complete movie details of a particular movie and passing them to the moviedetails.html page.
    movie=cursor.execute("SELECT * FROM movie WHERE movie_id={}".format(movie_id))
    movie=cursor.fetchall()
    actors=cursor.execute("SELECT name FROM actor WHERE actor_id IN (SELECT actor_id FROM movieactor WHERE movie_id={})".format(movie_id))
    actors=cursor.fetchall()
    genres=cursor.execute("SELECT name FROM genre WHERE genre_id IN (SELECT genre_id FROM moviegenre WHERE movie_id={})".format(movie_id))
    genres=cursor.fetchall()
    technicians=cursor.execute("SELECT name FROM technician WHERE technician_id IN (SELECT technician_id FROM movietechnician WHERE movie_id={})".format(movie_id))
    technicians=cursor.fetchall()
    return render_template('moviedetails.html',actors=actors,movie=movie,genres=genres,technicians=technicians)


@app.route('/update/<int:movie_id>')
def update(movie_id):
    #It is used for sending the data to the movie register form to display the data in the form.so that we can update the data.
    movie=cursor.execute("SELECT * FROM movie WHERE movie_id={}".format(movie_id))
    movie=cursor.fetchall()
    actors=cursor.execute("SELECT actor_id FROM movieactor WHERE movie_id={}".format(movie_id))
    actors=cursor.fetchall()
    actors=[i[0] for i in actors]
    genres=cursor.execute("SELECT genre_id FROM moviegenre WHERE movie_id={}".format(movie_id))
    genres=cursor.fetchall()
    genres=[i[0] for i in genres]
    technicians=cursor.execute("SELECT technician_id FROM movietechnician WHERE movie_id={}".format(movie_id))
    technicians=cursor.fetchall()
    technicians=[i[0] for i in technicians]
    tactors=cursor.execute("SELECT * FROM actor")
    tactors=cursor.fetchall()
    tgenres=cursor.execute("SELECT * FROM genre")
    tgenres=cursor.fetchall()
    ttechnicians=cursor.execute("SELECT * FROM technician")
    ttechnicians=cursor.fetchall()
    return render_template('updatemovie.html',movie=movie,genres=genres,actors=actors,technicians=technicians,tactors=tactors,tgenres=tgenres,ttechnicians=ttechnicians,sgenre=','.join(map(str, genres)),sactor=','.join(map(str, actors)),stechnician=','.join(map(str, technicians)))


@app.route('/updatemovie',methods=['POST'])
def updatemovie():
    #updating the movie details in the movie table and also updating the genre,actor and technician details in the respective tables using the POST method.
    movie_id=request.form['movie_id']
    name = request.form['name']
    year_of_release = request.form['year_of_release']
    average_rating = request.form['average_rating']
    genre_id = request.form['genre_id']
    actor_id = request.form['actor_id']
    technician_id = request.form['technician_id']
    query = "UPDATE movie SET name='{}',year_of_release={},average_rating={} WHERE movie_id={}".format(name,year_of_release,average_rating,movie_id)
    cursor.execute(query)
    conn.commit()
    cursor.execute("DELETE FROM MovieGenre WHERE movie_id={}".format(movie_id))
    conn.commit()
    cursor.execute("DELETE FROM MovieActor WHERE movie_id={}".format(movie_id))
    conn.commit()
    cursor.execute("DELETE FROM MovieTechnician WHERE movie_id={}".format(movie_id))
    conn.commit()
    for i in genre_id.split(","):
        query = "INSERT INTO MovieGenre (movie_id,genre_id) VALUES ({},{})".format(int(movie_id),int(i))
        cursor.execute(query)
        conn.commit()
    for i in actor_id.split(","):
        query = "INSERT INTO MovieActor (movie_id,actor_id) VALUES ({},{})".format(int(movie_id),int(i))
        cursor.execute(query)
        conn.commit()
    for i in technician_id.split(","):
        query = "INSERT INTO MovieTechnician (movie_id,technician_id) VALUES ({},{})".format(int(movie_id),int(i))
        cursor.execute(query)
        conn.commit()
    return redirect(url_for('showmovies'))


@app.route('/deletemovie/<int:movie_id>')
def delete(movie_id):
    #deleting the movie details from the movie table and also deleting the genre,actor and technician details from the respective tables.
    cursor.execute("DELETE FROM moviegenre WHERE movie_id={}".format(movie_id))
    cursor.execute("DELETE FROM movieactor WHERE movie_id={}".format(movie_id))
    cursor.execute("DELETE FROM movietechnician WHERE movie_id={}".format(movie_id))
    cursor.execute("DELETE FROM movie WHERE movie_id={}".format(movie_id))
    conn.commit()
    return redirect(url_for('showmovies'))


@app.route('/filter',methods=['GET'])
#filtering the movies based on the genre,actor and technician details provided by the user using the GET method.
def filter():
    genre_id=request.args.get('genre_id')
    actor_id=request.args.get('actor_id')
    technician_id=request.args.get('technician_id')
    genre_ids=genre_id.split(",")
    actor_ids=actor_id.split(",")
    technician_ids=technician_id.split(",")
    tactors=cursor.execute("SELECT * FROM actor")
    tactors=cursor.fetchall()
    tgenres=cursor.execute("SELECT * FROM genre")
    tgenres=cursor.fetchall()
    ttechnicians=cursor.execute("SELECT * FROM technician")
    ttechnicians=cursor.fetchall()
    conditions = []
    if genre_ids!=['']:
        conditions.append("movie_id IN (SELECT movie_id FROM moviegenre WHERE genre_id IN ({}))".format(','.join(genre_ids)))
        genre_ids=[int(i) for i in genre_ids]
    if actor_ids!=['']:
        conditions.append("movie_id IN (SELECT movie_id FROM movieactor WHERE actor_id IN ({}))".format(','.join(actor_ids)))
        actor_ids=[int(i) for i in actor_ids]
        
    if technician_ids!=['']:
        conditions.append("movie_id IN (SELECT movie_id FROM movietechnician WHERE technician_id IN ({}))".format(','.join(technician_ids)))
        technician_ids=[int(i) for i in technician_ids]
        
    sql_query = "SELECT * FROM movie"
    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return render_template('moviedashboard.html',movies=result,tgenres=tgenres,tactors=tactors,ttechnicians=ttechnicians,genres=genre_ids,actors=actor_ids,technicians=technician_ids,sgenre=genre_id,sactor=actor_id,stechnician=technician_id)


@app.route('/deleteactor/',methods=['POST'])
def deleteactor():
    #deleting the actor details from the actor table using the POST method.
    actor_id=request.form['uniqueNumber']
    cursor.execute("""
    DELETE FROM actor 
    WHERE actor_id = %s AND actor_id NOT IN (
        SELECT DISTINCT actor_id 
        FROM movieactor
    )""", (actor_id,))
    conn.commit()
    return jsonify({'success': True, 'message': 'Actor deleted successfully'})


@app.route('/deletetechnician/',methods=['POST'])
def deletetechnician():
    #deleting the technician details from the technician table using the POST method.
    technician_id=request.form['uniqueNumber']
    cursor.execute("""
    DELETE FROM technician 
    WHERE technician_id = %s AND technician_id NOT IN (
        SELECT DISTINCT technician_id 
        FROM movietechnician
    )""", (technician_id,))
    conn.commit()
    return jsonify({'success': True, 'message': 'Technician deleted successfully'})


@app.route('/deletegenre/',methods=['POST'])
def deletegenre():
    #deleting the genre details from the genre table using the POST method.
    genre_id=request.form['uniqueNumber']
    cursor.execute("""
    DELETE FROM genre 
    WHERE genre_id = %s AND genre_id NOT IN (
        SELECT DISTINCT genre_id 
        FROM moviegenre
    )""", (genre_id,))
    conn.commit()
    return jsonify({'success': True, 'message': 'Genre deleted successfully'})


@app.route('/actorassociatedmovies/<int:actor_id>')
def actorassociatemovies(actor_id):
    #retrieving the movies associated with a particular actor and passing them to the associatemovies.html page.
    cursor.execute("SELECT * FROM movie WHERE movie_id IN (SELECT movie_id FROM movieactor WHERE actor_id={})".format(actor_id))
    movies=cursor.fetchall()
    return render_template('associatemovies.html',movies=movies)


@app.route('/technicianassociatedmovies/<int:technician_id>')
def technicianassociatemovies(technician_id):
    #retrieving the movies associated with a particular technician and passing them to the associatemovies.html page.
    cursor.execute("SELECT * FROM movie WHERE movie_id IN (SELECT movie_id FROM movietechnician WHERE technician_id={})".format(technician_id))
    movies=cursor.fetchall()
    return render_template('associatemovies.html',movies=movies)


@app.route('/genreassociatedmovies/<int:genre_id>')
def genreassociatemovies(genre_id):
    #retrieving the movies associated with a particular genre and passing them to the associatemovies.html page.
    cursor.execute("SELECT * FROM movie WHERE movie_id IN (SELECT movie_id FROM moviegenre WHERE genre_id={})".format(genre_id))
    movies=cursor.fetchall()
    return render_template('associatemovies.html',movies=movies)


@app.route('/updateactor/<int:actor_id>')
def updateactor(actor_id):
    #retrieving the actor details from the actor table and passing them to the updatepeople.html page.To display them on the form so that we can update the data.
    cursor.execute("SELECT * FROM actor WHERE actor_id={}".format(actor_id))
    actor=cursor.fetchall()
    return render_template('update.html',data=actor,api="/updateactordetails")


@app.route('/updatetechnician/<int:technician_id>')
def updatetechnician(technician_id):
    #retrieving the technician details from the technician table and passing them to the updatepeople.html page.To display them on the form so that we can update the data.
    cursor.execute("SELECT * FROM technician WHERE technician_id={}".format(technician_id))
    technician=cursor.fetchall()
    return render_template('update.html',data=technician,api="/updatetechniciandetails")


@app.route('/updategenre/<int:genre_id>')
def updategenre(genre_id):
    #retrieving the genre details from the genre table and passing them to the updatepeople.html page.To display them on the form so that we can update the data.
    cursor.execute("SELECT * FROM genre WHERE genre_id={}".format(genre_id))
    genre=cursor.fetchall()
    return render_template('update.html',data=genre,api="/updategenredetails")


@app.route('/updateactordetails',methods=['POST'])
def updateactordetails():
    #updating the actor details in the actor table using the POST method.
    actor_id=request.form['id']
    name=request.form['name']
    cursor.execute("UPDATE actor SET name='{}' WHERE actor_id={}".format(name,actor_id))
    conn.commit()
    return redirect(url_for('showactors'))


@app.route('/updatetechniciandetails',methods=['POST'])
def updatetechniciandetails():
    #updating the technician details in the technician table using the POST method.
    technician_id=request.form['id']
    name=request.form['name']
    cursor.execute("UPDATE technician SET name='{}' WHERE technician_id={}".format(name,technician_id))
    conn.commit()
    return redirect(url_for('showtechnicians'))


@app.route('/updategenredetails',methods=['POST'])
def updategenredetails():
    #updating the genre details in the genre table using the POST method.
    genre_id=request.form['id']
    name=request.form['name']
    cursor.execute("UPDATE genre SET name='{}' WHERE genre_id={}".format(name,genre_id))
    conn.commit()
    return redirect(url_for('showgenres'))


if __name__ == '__main__':
    app.run(debug=True)
