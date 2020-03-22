# Importing flask libs
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
import json
from datetime import datetime
from emotion import get_emotion



# instantiate the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mom.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Track(db.Model):
    track_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(5), nullable=False)
    file = db.Column(db.String(1000), nullable=False)
    emotion = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Track%r'% self.track_id

    def asdict(self):
        res = {
            'id' : self.track_id,
            'name' : self.name,
            'file' : self.file,
            'duration' : self.duration,
            'emotion' : self.emotion
        }
        return res

class Playlist(db.Model):
    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_title = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.String(15), nullable=False)
    emotion = db.Column(db.String(10), default='404')

    def __repr__(self):
        return '<playlist%r'% self.playlist_id

class TrackGroup(db.Model):
    tg_id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, nullable=False, default=0)
    track_id = db.Column(db.Integer, nullable=False, default=0)
        
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    

# Here will be my models
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    trackTemp = []
    tracks = Track.query.all()
    for track in tracks:
        trackTemp.append(track.asdict())
    return render_template('index.html', current_user=current_user, tracks=trackTemp)


@app.route('/default_add_track', methods=['POST','GET'])
def default_add_track():
    track_to_delete = Track.query.delete()
    db.session.commit()
    track1 = Track(
        name= "All This Is - Joe L.'s Studio",
        duration = "2:46",
        file="https://raw.githubusercontent.com/muhammederdem/mini-player/master/mp3/1.mp3",
        emotion = "Angry"
         
    )
    track2 = Track(
        name= "The Forsaken - Broadwing Studio (Final Mix)",
        duration = "2:46",
        file="https://raw.githubusercontent.com/muhammederdem/mini-player/master/mp3/2.mp3",
        emotion = "Sad"
    )
    track3 = Track(
        name= "All The King's Men - Broadwing Studio (Final Mix)",
        duration = "2:46",
        file="https://raw.githubusercontent.com/muhammederdem/mini-player/master/mp3/3.mp3",
        emotion = "Surprise"
    )
    track4 = Track(
        name= "The Forsaken - Broadwing Studio (First Mix)",
        duration = "2:46",
        file="https://raw.githubusercontent.com/muhammederdem/mini-player/master/mp3/4.mp3",
        emotion = "Sad"
    )
    track5 = Track(
        name= "All The King's Men - Broadwing Studio (First Mix)",
        duration = "2:46",
        file="https://raw.githubusercontent.com/muhammederdem/mini-player/master/mp3/5.mp3",
        emotion = "Happy"
    )
    track6 = Track(
        name= "All This Is - Alternate Cuts",
        duration = "2:46",
        file="https://raw.githubusercontent.com/muhammederdem/mini-player/master/mp3/6.mp3",
        emotion = "Happy"
    )
    track7 = Track(
        name= "All The King's Men (Take 1) - Alternate Cuts",
        duration = "2:46",
        file="https://raw.githubusercontent.com/muhammederdem/mini-player/master/mp3/7.mp3",
        emotion = "Happy"
    )
    track8 = Track(
        name= "All The King's Men (Take 2) - Alternate Cuts",
        duration = "2:46",
        file="https://raw.githubusercontent.com/muhammederdem/mini-player/master/mp3/8.mp3",
        emotion = "Angry"
    )
    track9 = Track(
        name= "Magus - Alternate Cuts",
        duration = "2:46",
        file="https://raw.githubusercontent.com/muhammederdem/mini-player/master/mp3/9.mp3",
        emotion = "Happy"
    )
    db.session.add(track1)
    db.session.add(track2)
    db.session.add(track3)
    db.session.add(track4)
    db.session.add(track5)
    db.session.add(track6)
    db.session.add(track7)
    db.session.add(track8)
    db.session.add(track9)
    db.session.commit()
    return "Done..."
    # if request.method == 'POST':
    #     name = request.form['name']
    #     duration = request.form['duration']
    #     file = request.form['file']
    #     emotion = request.form['emotion']
    #     new_track = Track(
    #         name=name,
    #         duration=duration,
    #         file=file,
    #         emotion=emotion
    #     )
    #     # try:
    #     db.session.add(new_track)
    #     db.session.commit()
    #     return redirect('/')
    #     # except:
    #     #     return 'There was problem when adding track to database'

    # else:
    #     return render_template('add_track.html')

@app.route('/add_track', methods=['POST','GET'])
def add_track():
    if request.method == 'POST':
        name = request.form['name']
        duration = request.form['duration']
        file = request.form['file']
        emotion = request.form['emotion']
        new_track = Track(
            name=name,
            duration=duration,
            file=file,
            emotion=emotion
        )
        # try:
        db.session.add(new_track)
        db.session.commit()
        return redirect('/')
        # except:
        #     return 'There was problem when adding track to database'

    else:
        return render_template('add_track.html')

@app.route('/add_playlist', methods=['POST','GET'])
def add_playlist():
    if request.method == 'POST':
        name = request.form['name']
        emotion = request.form['emotion']
        new_playlist = Playlist(
            playlist_title=name,
            emotion=emotion,
            created_by=current_user.username
        )
        # try:
        db.session.add(new_playlist)
        db.session.commit()
        id = new_playlist.playlist_id
        return redirect('/add_tracks_to_playlist?playlist_id={}'.format(id))
        # except:
        #     return 'There was problem when adding track to database'

    else:
        return render_template('add_playlist.html')

@app.route('/add_tracks_to_playlist', methods=['POST','GET'])
def add_tracks_to_playlist():
    if request.method == 'POST':
        playlist_id = request.args.get('playlist_id')
        inputs = request.form.to_dict()
        for track_id in inputs:
            trackGroup = TrackGroup(
                track_id = int(track_id),
                playlist_id = playlist_id
            )
            db.session.add(trackGroup)
        
        db.session.commit()
        return redirect('/')
    else:
        tracks = Track.query.all()
        return render_template('add_tracks_to_playlist.html', tracks=tracks)



@app.route('/show_playlists', methods=['POST','GET'])
def show_playlists():
    playlists = Playlist.query.all()
    return render_template('show_playlists.html', playlists=playlists)

def convert_into_dict(track):
    res = {
        'id' : track.track_id,
        'name' : track.name,
        'file' : track.file,
        'duration' : track.duration,
        'emotion' : track.emotion
    }
    return res

@app.route('/play_playlist/<int:playlist_id>', methods=['POST','GET'])
def play_playlist(playlist_id):
    sql = 'select * from track where track.track_id in (select track_group.track_id from playlist inner join track_group on playlist.playlist_id=track_group.playlist_id where track_group.playlist_id={})'.format(playlist_id)
    print(sql)
    tracks = db.engine.execute(sql)
    trackTemp = []
    for track in tracks:
        trackTemp.append(convert_into_dict(track))
    return render_template('play_playlist.html', tracks = trackTemp)

@app.route('/delete_playlist/<int:playlist_id>')
def delete_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    db.session.delete(playlist)
    db.session.commit()
    trackGroup = TrackGroup.query.filter_by(playlist_id=playlist_id).delete()
    db.session.commit()
    return redirect('/show_playlists')

@app.route('/musicplayer', methods=['POST','GET'])
def musicplayer():
    mood = request.args.get('mood')
    if mood is None:
        print('mood is none')
        return render_template('index.html')
    filename = 'img/{}.png'.format(mood)
    print(mood)
    trackTemp = []
    tracks = Track.query.all()
    for track in tracks:
        trackTemp.append(track.asdict())
    return render_template('index.html', filename=filename, current_user=current_user, tracks=trackTemp)


@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form=form)  

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/predict')
def predict():
    label = get_emotion()    
    return redirect('/musicplayer?mood='+label)

if __name__== "__main__":
    app.run(debug=True)