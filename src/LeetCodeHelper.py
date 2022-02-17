import urllib3, json, re, requests, argparse, os
from bs4 import BeautifulSoup as bs
from config import *
from Question import Question

class LeetcodeHelper():
    def __init__(self, refresh_data: bool):
        self.language_extension = {"C++": "cpp", "Python3": "py"}
        self.csrftoken = None
        self.data = None
        
        if refresh_data: 
            # fetch all problem data from leetcode.com again and store as data.json
            self.csrftoken = self.get_csrftoken()
            self.data = self.read_data_from_remote(RAW_DATA_FILE_PATH, self.csrftoken)
            print("Successfully fetched all problem data from leetcode.com")
            print("Data stored at {}".format(RAW_DATA_FILE_PATH))
        else:
            self.data = self.read_data_from_local_file(RAW_DATA_FILE_PATH)
            print("Successfully read all problem data from {}".format(RAW_DATA_FILE_PATH))

        self.total_problem_count = self.data["data"]["problemsetQuestionList"]["total"]
        self.question_metadata = self.data["data"]["problemsetQuestionList"]["questions"]


        # all question instances here
        self.questions = {}

    def build_working_dir_for_questions(self):
        print("You have {} questions".format(self.questions))
        if len(self.questions) == 0:
            return
        for i, q in self.questions.items():
            if os.path.isdir("solutions/{}".format(q.title_slug)):
                print("Solution dir found.")
                rec = len([n for n in os.listdir('.') if os.path.isfile(n)])//2
                print("Creating code snippet version -{}".format(rec))
                for lang, snippet in q.code_snippet.items():
                    extension = ".py" if lang == "Python3" else ".cpp"
                    with open(os.path.join("solutions/", q.title_slug, q.title_slug+str(rec)+extension), "w+") as f:
                        f.write(snippet)
            else:
                print("Creating solution dir id={}".format(i))
                os.makedirs(os.path.join("solutions", q.title_slug))

                print("Creating README.md")
                with open(os.path.join("solutions", q.title_slug, "README.md"), "w+") as f:
                    f.write(q.description)

                print("Creating sample input")
                with open(os.path.join("solutions", q.title_slug, "sample_input.json"), "w+") as f:
                    f.write(json.dumps(q.sample_input))

                print("Creating code snippet")
                for lang, snippet in q.code_snippet.items():
                    extension = ".py" if lang == "Python3" else ".cpp"
                    with open(os.path.join("solutions", q.title_slug, q.title_slug+extension), "w+") as f:
                        f.write(snippet)

    def build_question(self, q_id: int) :
        self.questions[q_id] = Question(metadata=self.question_metadata[q_id-1])

    def delete_question(self, q_id: int) :
        del self.questions[q_id]
        
    def get_single_built_question(self, q_id: int):
        try:
            return self.questions[q_id]
        except:
            exit("**ERROR*** This question (id={}) hasn't been built yet".format(q_id))

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

        

