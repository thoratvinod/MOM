// Mythium Archive: https://archive.org/details/mythium/
var jsTracks
function getTracks(tracks){
    return tracks
}
function setTracks(tracks){
    jsTracks = tracks
}
console.log(jsTracks)
jQuery(function ($) {
  'use strict'
  var supportsAudio = !!document.createElement('audio').canPlayType;
  if (supportsAudio) {
      // initialize plyr
      var player = new Plyr('#audio1', {
          controls: [
              'restart',
              'play',
              'progress',
              'current-time',
              'duration',
              'mute',
              'volume',
              'download'
          ]
      });
      // initialize playlist and controls
      var index = 0,
          playing = false,
          mediaPath = 'https://raw.githubusercontent.com/muhammederdem/mini-player/master/mp3/',
          extension = '',
          tracks = [{
              "track": 1,
              "name": "All This Is - Joe L.'s Studio",
              "duration": "2:46",
              "file": "1"
          }, {
              "track": 2,
              "name": "The Forsaken - Broadwing Studio (Final Mix)",
              "duration": "8:30",
              "file": "2"
          }, {
              "track": 3,
              "name": "All The King's Men - Broadwing Studio (Final Mix)",
              "duration": "5:01",
              "file": "3"
          }, {
              "track": 4,
              "name": "The Forsaken - Broadwing Studio (First Mix)",
              "duration": "8:31",
              "file": "4"
          }, {
              "track": 5,
              "name": "All The King's Men - Broadwing Studio (First Mix)",
              "duration": "5:05",
              "file": "5"
          }, {
              "track": 6,
              "name": "All This Is - Alternate Cuts",
              "duration": "2:48",
              "file": "6"
          }, {
              "track": 7,
              "name": "All The King's Men (Take 1) - Alternate Cuts",
              "duration": "5:44",
              "file": "7"
          }, {
              "track": 8,
              "name": "All The King's Men (Take 2) - Alternate Cuts",
              "duration": "5:26",
              "file": "8"
          }, {
              "track": 9,
              "name": "Magus - Alternate Cuts",
              "duration": "5:46",
              "file": "9"
          }],
          buildPlaylist = $.each(tracks, function(key, value) {
              var trackNumber = value.track,
                  trackName = value.name,
                  trackDuration = value.duration;
              if (trackNumber.toString().length === 1) {
                  trackNumber = '0' + trackNumber;
              }
              $('#plList').append('<li> \
                  <div class="plItem"> \
                      <span class="plNum">' + trackNumber + '.</span> \
                      <span class="plTitle">' + trackName + '</span> \
                      <span class="plLength">' + trackDuration + '</span> \
                  </div> \
              </li>');
          }),
          trackCount = tracks.length,
          npAction = $('#npAction'),
          npTitle = $('#npTitle'),
          audio = $('#audio1').on('play', function () {
              playing = true;
              npAction.text('Now Playing...');
          }).on('pause', function () {
              playing = false;
              npAction.text('Paused...');
          }).on('ended', function () {
              npAction.text('Paused...');
              if ((index + 1) < trackCount) {
                  index++;
                  loadTrack(index);
                  audio.play();
              } else {
                  audio.pause();
                  index = 0;
                  loadTrack(index);
              }
          }).get(0),
          btnPrev = $('#btnPrev').on('click', function () {
              if ((index - 1) > -1) {
                  index--;
                  loadTrack(index);
                  if (playing) {
                      audio.play();
                  }
              } else {
                  audio.pause();
                  index = 0;
                  loadTrack(index);
              }
          }),
          btnNext = $('#btnNext').on('click', function () {
              if ((index + 1) < trackCount) {
                  index++;
                  loadTrack(index);
                  if (playing) {
                      audio.play();
                  }
              } else {
                  audio.pause();
                  index = 0;
                  loadTrack(index);
              }
          }),
          li = $('#plList li').on('click', function () {
              var id = parseInt($(this).index());
              if (id !== index) {
                  playTrack(id);
              }
          }),
          loadTrack = function (id) {
              $('.plSel').removeClass('plSel');
              $('#plList li:eq(' + id + ')').addClass('plSel');
              npTitle.text(tracks[id].name);
              index = id;
              audio.src = mediaPath + tracks[id].file + extension;
              updateDownload(id, audio.src);
          },
          updateDownload = function (id, source) {
              player.on('loadedmetadata', function () {
                  $('a[data-plyr="download"]').attr('href', source);
              });
          },
          playTrack = function (id) {
              loadTrack(id);
              audio.play();
          };
      extension = audio.canPlayType('audio/mpeg') ? '.mp3' : audio.canPlayType('audio/ogg') ? '.ogg' : '';
      loadTrack(index);
  } else {
      // no audio support
      $('.column').addClass('hidden');
      var noSupport = $('#audio1').text();
      $('.container').append('<p class="no-support">' + noSupport + '</p>');
  }
});
