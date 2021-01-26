from flask import Flask, render_template, request

import tmdb_client

app = Flask(__name__)

MOVIE_LISTS = [
    ("now_playing", "Now Playing"),
    ("popular", "Popular"),
    ("top_rated", "Top Rated"),
    ("upcoming", "Upcoming")
]


@app.route("/")
def homepage():
    selected_list = request.args.get("list_type", "popular")
    if selected_list not in [x[0] for x in MOVIE_LISTS]:
        selected_list = "popular"
    movies = tmdb_client.get_movies(12, selected_list)
    return render_template("homepage.html", movies=movies,
                           current_list=selected_list, all_lists=MOVIE_LISTS)


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)[:8]
    return render_template("movie_details.html", movie=details, cast=cast)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

if __name__ == "__main__":
    app.run(debug=True)
