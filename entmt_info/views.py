from django.shortcuts import render


# 상세 정보 페이지
def e_detail(request):

    return render(request, 'entmt_info/detail.html')


# 검색 결과 페이지
def e_results(request):

    return render(request, 'entmt_info/results.html')
