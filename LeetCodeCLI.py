import urllib3, json, re, requests, argparse
from bs4 import BeautifulSoup as bs
# from utils import *
# from cfg import *
# from create_snippet import *

class LeetcodeCLI():
    def __init__(self, refresh_data: bool):
        super().__init__()
        self.language_extension = {"cpp": "cpp", "python": "py"}
        self.DATA_FILE_PATH = "data.json"
        self.csrftoken = None
        self.data = None
        
        if refresh_data: 
            # fetch all problem data from leetcode.com again and store as data.json
            self.csrftoken = self.get_csrftoken()
            self.data = self.read_data_from_remote(self.DATA_FILE_PATH, self.csrftoken)
            print("Successfully fetched all problem data from leetcode.com")
            print("Data stored at {}".format(self.DATA_FILE_PATH))
        else:
            self.data = self.read_data_from_local_file(self.DATA_FILE_PATH)
            print("Successfully read all problem data from {}".format(self.DATA_FILE_PATH))

        self.total_problem_count = self.data["data"]["problemsetQuestionList"]["total"]
        self.problem_list = self.data["data"]["problemsetQuestionList"]["questions"]
            
    def create_code_template(self, question_id):
        # print(self.problem_list[question_id-1])
        q = self.problem_list[question_id-1]

        acRate = int(q["acRate"])
        difficulty = q["difficulty"]
        freqBar = q["freqBar"]
        questionId = q["frontendQuestionId"]
        isFavor = q["isFavor"]
        paidOnly = q["paidOnly"]
        status = q["status"]
        title = q["title"]
        titleSlug = q["titleSlug"]
        topicTags = [obj["slug"] for obj in q["topicTags"]]
        hasSolution = q["hasSolution"]
        hasVideoSolution = q["hasVideoSolution"]


        '''
        In each problem: 

        acRate: 48.239787883036115
        difficulty: Easy
        freqBar: None
        frontendQuestionId: 1
        isFavor: False
        paidOnly: False
        status: None
        title: Two Sum
        titleSlug: two-sum
        topicTags: [{'name': 'Array', 'id': 'VG9waWNUYWdOb2RlOjU=', 'slug': 'array'}, {'name': 'Hash Table', 'id': 'VG9waWNUYWdOb2RlOjY=', 'slug': 'hash-table'}]
        hasSolution: True
        hasVideoSolution: True
        '''

        # problem url format:  https://leetcode.com/problems/<titleSlug>

    def get_csrftoken(self):
        http = urllib3.PoolManager()
        r = http.request(
            'GET',
            'https://leetcode.com/problemset/all/',
            redirect=False
        )
        if r.status != 302:
            raise RuntimeError('Fail to get csrftoken! status: %d, data: %s' % (r.status, r.data))
        match_obj = re.search('csrftoken=(\S+); ', r.headers['Set-Cookie'])
        if match_obj:
            return match_obj.group(1)
        else:
            raise RuntimeError('Fail to parse csrftoken from headers! headers: %s' % r.headers)


    def fetch(self, csrftoken, limit=50):
        http = urllib3.PoolManager()
        cookie = 'csrftoken={}'.format(csrftoken)
        data = {
            'query': 'query problemsetQuestionList($categorySlug:String,$limit:Int,$skip:Int,$filters:QuestionListFilterInput){problemsetQuestionList:questionList(categorySlug:$categorySlug limit:$limit skip:$skip filters:$filters){total:totalNum questions:data{acRate difficulty freqBar frontendQuestionId:questionFrontendId isFavor paidOnly:isPaidOnly status title titleSlug topicTags{name id slug}hasSolution hasVideoSolution}}}',
            'variables': {
                'categorySlug': '',
                'skip': 0,
                'filters': {},
                'limit': limit,
            },
        }
        encoded_data = json.dumps(data).encode('utf-8')
        r = http.request(
            'POST',
            'https://leetcode.com/graphql/',
            body=encoded_data,
            headers={
                'Content-Type': 'application/json',
                'cookie': cookie,
            },
        )
        if r.status != 200:
            print(r.status)
            raise RuntimeError("Fail to fetch problems! status: {}, data: {}".format((r.status, r.data)))
        response = json.loads(r.data)
        return response


    def read_data_from_remote(self, output_file, csrftoken):
        data = self.fetch(csrftoken)
        question_count = data["data"]["problemsetQuestionList"]["total"]
        data = self.fetch(csrftoken, limit=question_count)

        with open(output_file, 'w') as f:
            f.write(json.dumps(data))

        return data

    def read_data_from_local_file(self, input_file):
        with open(input_file, 'r') as f:
            data = json.load(f)
        return data


if __name__ == '__main__':
    LC = LeetcodeCLI(refresh_data=False)
    LC.create_code_template(1)



