import json
import math
import urllib.request
import urllib.error
import urllib.parse

naver_client_id = "Input My Naver Open API application ID"
naver_client_secret = "Input My Naver Open API application Secret"


def naver_blog_crawling(search_blog_keyword, display_count):
    search_result_blog_page_count = get_blog_search_result_pagination_count(search_blog_keyword, display_count)
    get_blog_post_url(search_blog_keyword, display_count, search_result_blog_page_count)


def get_blog_search_result_pagination_count(search_blog_keyword, display_count):
    encode_search_keyword = urllib.parse.quote(search_blog_keyword)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encode_search_keyword
    request = urllib.request.Request(url)

    request.add_header("X-Naver-Client-Id", naver_client_id)
    request.add_header("X-Naver-Client-Secret", naver_client_secret)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()

    if response_code is 200:
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode('utf-8'))

        if response_body_dict['total'] == 0:
            blog_pagination_count = 0
        else:
            blog_pagination_total_count = math.ceil(response_body_dict['total'] / int(display_count))

            if blog_pagination_total_count >= 1000:
                blog_pagination_count = 1000
            else:
                blog_pagination_count = blog_pagination_total_count

            print("키워드 \'" + search_blog_keyword + "\'에 해당하는 포스팅 수 : " + str(response_body_dict['total']))

        return blog_pagination_count


def get_blog_post_url(search_blog_keyword, display_count, search_result_blog_page_count):
    f = open('urls.txt', 'a')   # URLs
    encode_search_blog_keyword = urllib.parse.quote(search_blog_keyword)

    for i in range(1, search_result_blog_page_count + 1):
        url = "https://openapi.naver.com/v1/search/blog?query=" + encode_search_blog_keyword + "&display=" + str(
            display_count) + "&start=" + str(i)

        request = urllib.request.Request(url)

        request.add_header("X-Naver-Client-Id", naver_client_id)
        request.add_header("X-Naver-Client-Secret", naver_client_secret)

        response = urllib.request.urlopen(request)
        response_code = response.getcode()

        if response_code is 200:
            response_body = response.read()
            response_body_dict = json.loads(response_body.decode('utf-8'))

            for j in range(0, len(response_body_dict['items'])):
                try:
                    blog_post_url = response_body_dict['items'][j]['link'].replace("amp;", "")
                    blog_post_url = blog_post_url.replace("https://blog.naver.com/", "https://m.blog.naver.com/PostView.nhn?blogId=").split('?')
                    blog_post_url = blog_post_url[0] + '?' + blog_post_url[1] + '&logNo=' + blog_post_url[-1].split('=')[-1]
                    # print(blog_post_url)
                    f.write(blog_post_url + '\n')
                except:
                    j += 1
    f.close()


if __name__ == '__main__':
    keyword = input()   # 썬팅 후기 -사무실 -아파트
    naver_blog_crawling(keyword, 100)