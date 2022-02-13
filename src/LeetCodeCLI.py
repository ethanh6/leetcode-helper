import urllib3, json, re, requests, argparse
from bs4 import BeautifulSoup as bs
from config import *

class LeetcodeCLI():
    def __init__(self, refresh_data: bool):
        self.language_extension = {"C++": "cpp", "Python3": "py"}
        self.csrftoken = None
        self.data = None
        
        if refresh_data: 
            # fetch all problem data from leetcode.com again and store as data.json
            self.csrftoken = self.get_csrftoken()
            self.data = self.read_data_from_remote(DATA_FILE_PATH, self.csrftoken)
            print("Successfully fetched all problem data from leetcode.com")
            print("Data stored at {}".format(DATA_FILE_PATH))
        else:
            self.data = self.read_data_from_local_file(DATA_FILE_PATH)
            print("Successfully read all problem data from {}".format(DATA_FILE_PATH))

        self.total_problem_count = self.data["data"]["problemsetQuestionList"]["total"]
        self.question_metadata = self.data["data"]["problemsetQuestionList"]["questions"]
            

    def get_question_starter(self, question_id: int, language="Python3", showHints=False, showSimilar=False) :

        q = self.question_metadata[question_id-1]

        # usable data in q (q is a dictionaly)
        # acRate: 48.239787883036115
        # difficulty: Easy
        # freqBar: None
        # frontendQuestionId: 1
        # isFavor: False
        # paidOnly: False
        # status: None
        # title: Two Sum
        # titleSlug: two-sum
        # topicTags: [{'name': 'Array', 'id': 'VG9waWNUYWdOb2RlOjU=', 'slug': 'array'}, {'name': 'Hash Table', 'id': 'VG9waWNUYWdOb2RlOjY=', 'slug': 'hash-table'}]
        # hasSolution: True
        # hasVideoSolution: True


        # get more data from the website
        data[QUESTION_KEY][QUESTION_QUERY_KEY] = q["titleSlug"]
        res = requests.post(WEBSITE_URL + QUERY_EXTENTION, json = data).json()['data']['question']

        # usable data in res (res is a dictionary)
        # questionId, questionFrontendId, boundTopicId, title, titleSlug,
        # content, translatedTitle, translatedContent, isPaidOnly,
        # difficulty, likes, dislikes, isLiked, similarQuestions, contributors,
        # langToValidPlayground, topicTags, companyTagStats, codeSnippets,
        # stats, hints, solution, status, sampleTestCase, metaData,
        # judgerAvailable, judgeType, mysqlSchemas, enableRunCode,
        # enableTestMode, envInfo, libraryUrl, __typename,
        
        description = bs(res['content'], 'lxml').get_text()
        description += "\n\n"

        # add hints
        if showHints :
            description += "\n===  Hints === \n"
            for h in res['hints'] :
                description += h + "\n"

        # add similar questions
        if showSimilar :
            description += "\n=== Similar Questions === \n"
            similar_questions = [q["titleSlug"] for q in json.loads(res['similarQuestions'])]
            for s in similar_questions:
                description += s + "\n"

        # add link to leetcode website
        description += "\n=== Question url === \n" + WEBSITE_URL + PROBLEM_EXTENTION + q["titleSlug"]

        # get code snippets
        code_snippet = "".join([c['code'] if c['lang'] == language else "" for c in res['codeSnippets']])

        # get sample test case input as keyword arg to the solution
        sample_testcase = res["sampleTestCase"].split("\n")

        # parse the parameter name 
        arg_name = [i['name'] for i in json.loads(res["metaData"])["params"]]

        # address the parameter type 
        print(json.loads(res["metaData"])["params"])

        sample_input = {k:json.loads(v) for k, v in zip(arg_name, sample_testcase)}
        print(sample_input)

        # print(description)
        print(code_snippet)


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
    LC.get_question_starter(1, language="Python3", showHints=True, showSimilar=True)


