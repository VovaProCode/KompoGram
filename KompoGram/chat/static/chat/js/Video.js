function video_player(){
    $('.player').off()
    const videodivs = $('.player');
    console.log(videodivs)
    let activePlayer
    videodivs.each(function(index, player) {
        const peaky_play_pause = $(this).find(".play-pause_button");
        const video = $(this).find("video");
        const full_screen = $(this).find(".full_screen");
        const mini_player = $(this).find(".mini_player");
        const volumediv = $(this).find(".volume");
        const volume_range = $(this).find(".volume_range");
        const time = $(this).find(".duration_div");
        const end_time = $(this).find(".end_time");
        const start_time = $(this).find(".start_time");
        const controls = $(this).find(".controls");
        const controls_div = $(this).find(".controls_div");
        const subtitres = $(this).find(".subtitres");
        const speed = $(this).find(".speed");
        const preview = $(this).find(".preview");
        const thumbnail = $(this).find(".thumb_indicator");
        const timeline_div = $(this).find(".timeline_div");
        const next_series1 = $(this).find(".next_button1");
        const next_series2 = $(this).find(".next_button2");
        const button_series = $(this).find(".button_serias");
        const preview_time = $(this).find(".preview-time");
        let activePlayer
        // Здесь добавьте обработчики событий для каждого плеера, используя найденные элементы
        // Например:

        player_zminna = index

        $(document).on("keydown", function(e) {
            console.log('keydosdasd')
            console.log(player_zminna)
            console.log(activePlayer)
            if (activePlayer == player_zminna){
                console.log('kaaaaaaaaaaaaaaaaa')
                switch(e.key.toLowerCase()){
                    case ' ':
                        toggleplay()
                    case "k":
                        toggleplay()
                        break
                    case "f":
                        togglefull()
                        break
                    case "i":
                        togglemini()
                        break
                    case "m":
                        togglevolume()
                        break
                    case "arrowleft":
                        skip(-5)
                        break
                    case "arrowright":
                        skip(5)
                        break
                    case "arrowdown":
                        volume_set(-0.1)
                        break
                    case "arrowup":
                        volume_set(0.1)
                        break
                }
            }
        })
        video.on("dblclick", togglefull)
        var A;

        video.on("timeupdate", function() {
            videoo = video[0]
            start_time.text(formatDuration(videoo.currentTime))
            const percent = videoo.currentTime / videoo.duration
            timeline_div.css("--progress-position", percent)
        })

        timeline_div.on("mousemove", handletime)
        timeline_div.on("mousedown", toggleScrubbing)
        $(document).on("mouseup", function(e) {
            if (isScrubbing) toggleScrubbing(e)
        })
        $(document).on("mousemove", function(e) {
            if (isScrubbing) handletime(e)
        })

        let isScrubbing = false
        let wasPaused
        function toggleScrubbing(e) {
            videoo = video[0]
            const rect = timeline_div.offset().left;
            const width = timeline_div.width();
            const percent = Math.min(Math.max(0, e.pageX - rect), width) / width
            isScrubbing = (e.buttons & 1) === 1
            $(this).toggleClass("scrubbing", isScrubbing)
            if (isScrubbing) {
                wasPaused = video.prop('paused');
                console.log(wasPaused)
                if (!wasPaused) {
                    var playPromise = videoo.play();
                    if (playPromise !== undefined) {
                        playPromise.then(_ => {
                            videoo.pause();
                            console.log('laaaaaaaaaaaa')
                        })
                    }
                }
            } else {
                videoo.currentTime = percent * videoo.duration;
                console.log(wasPaused)
                if (!wasPaused) {
                    console.log('igrae')
                    videoo.play();
                }
            }
            handletime(e)
        }

        function handletime(e) {
            videoo = video[0]
            const rect = timeline_div.offset().left;
            const width = timeline_div.width();
            const percent = Math.min(Math.max(0, e.pageX - rect), width) / width

            const time = percent * videoo.duration;
            preview_time.text(formatDuration(time))

            timeline_div.css("--preview-position", percent)

            if(isScrubbing){
                e.preventDefault()
                timeline_div.css("--progress-position", percent)
            }
        }

        speed.on("click", togglespeed)

        function togglespeed(){
            videoo = video[0]
            let speedplay = videoo.playbackRate + .25
            if (speedplay > 2) speedplay =.25
            videoo.playbackRate = speedplay
            speed.text(`${speedplay}x`)
        }

        function toggleplay(){
            videoo = video[0]
            video.prop("paused") ? video.trigger('play') : video.trigger('pause')
            if (videoo.paused === false){
                activePlayer = index;
                console.log('daaaaaaaaaaaaaaaaaaa')
                console.log(activePlayer)
            }else{
                activePlayer = 'neeeee'
            }
        }
        video.on("play", function() {
            player.classList.remove("paused")
        })
        video.on("pause", function() {
            player.classList.add("paused")
        })

        full_screen.on("click", togglefull)
        mini_player.on("click", togglemini)

         function togglefull() {
            const videoElement = player; // Получаем DOM-элемент video из jQuery-объекта
            if (videoElement.requestFullscreen) {
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                } else {
                    videoElement.requestFullscreen();
                }
            }
        }

        function togglemini (){
            videoo = video[0]
            if (video.hasClass("mini-player")){
                document.exitPictureInPicture()
            }else{
                videoo.requestPictureInPicture()
            }
        }

        $(this).on("fullscreenchange", function() {

            $(this).toggleClass("full_screen", $(this).fullscreenElement)
        })

        peaky_play_pause.on("click", toggleplay)
        video.on("click", toggleplay)

        video.on("enterpictureinpicture", function() {
            $(this).addClass("mini_player")
        })
        video.on("leavepictureinpicture", function() {
            $(this).removeClass("mini_player")
        })

        volumediv.on("click", togglevolume)
        volume_range.on("input", function(e) {
            videoo = video[0]
            videoo.volume = e.target.value
            videoo.muted = e.target.value === 0
        })

        function togglevolume() {
            videoo = video[0]
            videoo.muted = !videoo.muted
        }

        video.on("volumechange", function() {
            videoo = video[0]
            volume_range.val(videoo.volume)
            let volumelevel
            if (videoo.muted || videoo.volume == 0){
                volume_range.val(0)
                volumelevel = "muted"
            } else if (videoo.volume >= 0.5) {
                volumelevel = "high"
            } else {
                volumelevel = "low"
            }
            player.dataset.volumelevel = volumelevel
        })

        video.on("loadedmetadata", function() {
            const videoo = video[0]
            console.log('adasda')
            end_time.text(formatDuration(videoo.duration))
        })

        const learnzero = new Intl.NumberFormat(undefined, {
            minimumIntegerDigits: 2
        })

        function volume_set(count) {
            videoo = video[0]
            volume_video = videoo.volume
            console.log(volume_video)
            if (volume_video < 0.1){
                if (count === -0.1){
                    console.log('laaaaaaaaaaa')
                    videoo.volume = 0
                }else if (count === 0.1){
                    console.log('laaaaaaaaaaa')
                    videoo.volume =+ count
                }
            }else if (volume_video > 0.9){
                if (count === 0.1){
                    console.log('да')
                    videoo.volume = 1
                }else if(count === -0.1){
                    videoo.volume += count
                }
            }else{
                videoo.volume += count
            }

        }

        function formatDuration(time){
            const sec = Math.floor(time % 60)
            const minuts = Math.floor(time / 60 ) % 60
            const hours = Math.floor(time / 3600)
            if (hours === 0) {
                return `${minuts}:${learnzero.format(sec)}`
            }else{
                return `${hours}:${learnzero.format(
                    minuts
                    )}:${learnzero.format(sec)}`
            }
        }

        function skip(seconds) {
            videoo = video[0]
            videoo.currentTime += seconds
        }

        $(this).on("fullscreenchange", function() {
            if ($(this).fullscreenElement) {
                setTimeout(function(){
                    for(var i = 0; i < 3; i++){
                        controls.css('display', "none");
                        controls.css('cursor', "none");
                    }
                }, 3000)
            }else{
                controls.css('display', "flex")
            }
        });

        var timeout = setTimeout(hideControls, 3000);

        // Добавляем обработчик событий на движение мыши и нажатие клавиш на клавиатуре
        $(this).on('mousemove', resetTimeout);
        $(this).on('keypress', resetTimeout);

        // Функция для скрытия элементов управления видео
        function hideControls() {
          timeline_div.css('display', 'none');
          controls.css('display', 'none');
          video.css('cursor', "none");
          controls.css('cursor', "auto");
          controls_div.css('opacity', "0");
        }

        // Функция для показа элементов управления видео
        function showControls() {
         timeline_div.css('display', 'flex');
         controls.css('display', 'flex');
         video.css('cursor', "auto");
         controls.css('cursor', "auto");
         controls_div.css('background', "linear-gradient(to top, rgba(0, 0, 0, .75), transparent)");
         controls_div.css('opacity', "1");
        }

        // Функция для сброса таймера
        function resetTimeout() {
          clearTimeout(timeout);
          showControls();
          timeout = setTimeout(hideControls, 3000);
        }

        //next_series1.addEventListener("click", () => {
        //    video.src = "images/peaky_video.mp4"
        //})
        //next_series2.addEventListener("click", () => {
        //    video.src = "images/video.mp4"
        //})
    });
}
video_player()