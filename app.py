from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# Mock movie data
movies = [
    {'title': 'Pirates of the Caribbean', 'genre': 'Adventure', 'imageUrl': 'static/images/imagepoc.jpg', 'moviePath': 'static/videos/Pirates.mp4'},
    {'title': 'Movie 2', 'genre': 'Comedy', 'imageUrl': 'static/images/movie2.jpg', 'moviePath': 'static/videos/movie2.mp4'},
    {'title': 'Movie 3', 'genre': 'Drama', 'imageUrl': 'static/images/movie3.jpg', 'moviePath': 'static/videos/movie3.mp4'},
    {'title': 'Movie 4', 'genre': 'Horror', 'imageUrl': 'static/images/movie4.jpg', 'moviePath': 'static/videos/movie4.mp4'},
    {'title': 'Movie 5', 'genre': 'Adventure', 'imageUrl': 'static/images/movie5.jpg', 'moviePath': 'static/videos/movie5.mp4'}
]


# API endpoint to get movies
@app.route('/api/movies', methods=['GET'])
def get_movies():
    genre = request.args.get('genre', '')
    search = request.args.get('search', '').lower()
    filtered_movies = [
        movie for movie in movies
        if (not genre or movie['genre'] == genre) and
           (not search or search in movie['title'].lower())
    ]

    return jsonify(filtered_movies)

@app.route('/watch', methods=['GET'])
def watch_movie():
    title = request.args.get('title')
    movie = next((movie for movie in movies if movie['title'] == title), None)
    
    if movie:
        return f'''
        <html>
        <body>
            <h1>Watching {movie['title']}</h1>
            <video width="800" controls>
                <source src="{movie['moviePath']}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </body>
        </html>
        '''
    else:
        return "Movie not found", 404

@app.route('/download', methods=['GET'])
def download_movie():
    title = request.args.get('title')
    movie = next((movie for movie in movies if movie['title'] == title), None)
    
    if movie:
        filename = movie['moviePath'].split('/')[-1]  # Extract the filename from the path
        return send_from_directory('static/videos', filename, as_attachment=True)
    else:
        return "Movie not found", 404

# Serve static files
@app.route('/<path:path>', methods=['GET'])
def static_files(path):
    return send_from_directory('', path)

# Serve the homepage
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
