$(document).ready(function() {

    // 홈 섹션 표시
    $('#home').show();

    // 네비게이션 링크 클릭 이벤트
    $('nav ul li a').on('click', function(event) {
        event.preventDefault();
        var targetSection = $(this).attr('href');
        $('.content section').hide();   // 모든 섹션 숨기기
        $(targetSection).show(); // 클릭한 섹션만 표시
    });
});

