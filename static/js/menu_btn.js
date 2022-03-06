
function to_import(){
    document.location.href = '/entmt_info/import/'
}

function import_genres(){
    document.location.href = '/entmt_info/import_genre/'
    // tmdb에서 장르 받아오기
}

function import_movie(){
    document.location.href = '/entmt_info/import_movie/'
    // tmdb에서 영화 정보 받아오기
}

function import_tv(){
    document.location.href = '/entmt_info/import_tv/'
    // tmdb에서 시리즈 정보 받아오기
}

function click_like(){
    // button의 속성이 like_false라면 << 나중에 detail에 표시해줄때도 like_false 설정해줘야겠네
    // console.log($('#like_count_button').css("background-color"))
    // if ($('#like_count_button').css("background-color") == 'rgb(255, 105, 180)'){
    //     console.log('으악')
    // }
}