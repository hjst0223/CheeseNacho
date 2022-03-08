
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

// function delete_comment() {
//     $.ajax({
//         async: true,
//         url: "/entmt_info/delete_comment/",
//         type: 'GET',
//         data: {
//             // comment_id: $('#comment_status.id').text()
//         },
//         dataType: 'json',
//         timeout: 3000,
//
//         success: function() {
//             alert('댓글 삭제 성공')
//         },
//         error: function() {
//             alert('삭제 실패!' + $('#comment_status').text())
//         }
//     })
// }

// function update_comment() {
//     document.location.href = '/entmt_info/update_comment/'
//
//     $.ajax({
//         async: true,
//         url: "/entmt_info/update_comment/",
//         type: 'GET',
//         data: {
//             comment_id: $('#comment_id').text()
//         },
//         dataType: 'json',
//         timeout: 3000,
//
//         success: function() {
//             alert('댓글 수정 성공')
//         },
//         error: function() {
//             alert('수정 실패!' + $('#comment_id').text())
//         }
//     })
// }