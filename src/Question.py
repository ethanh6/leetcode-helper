import urllib3, json, requests
from bs4 import BeautifulSoup as bs
from config import *

class Question():
    def __init__(self, metadata):
        # usable data in self.metadata (q is a dictionaly)
        # acRate, difficulty, freqBar, frontendQuestionId, isFavor,
        # paidOnly, status, title, titleSlug, topicTags, hasSolution,
        # hasVideoSolution
        self.metadata = metadata
        self.title= metadata["title"]
        self.title_slug = metadata["titleSlug"]
        self.question_id = metadata["frontendQuestionId"]
        self.difficulty = metadata["difficulty"]
        self.description = ""
        self.code_snippet = ""
        self.sample_input = None
        self.topic_tags = None

        # get more data from the website
        data[QUESTION_KEY][QUESTION_QUERY_KEY] = self.title_slug
        self.res = requests.post(WEBSITE_URL + QUERY_EXTENTION, json = data).json()['data']['question']

        self.topic_tags = [i["slug"] for i in self.res["topicTags"]]

        # usable data in res (res is a dictionary)
        # questionId, questionFrontendId, boundTopicId, title, titleSlug,
        # content, translatedTitle, translatedContent, isPaidOnly,
        # difficulty, likes, dislikes, isLiked, similarQuestions, contributors,
        # langToValidPlayground, topicTags, companyTagStats, codeSnippets,
        # stats, hints, solution, status, sampleTestCase, metaData,
        # judgerAvailable, judgeType, mysqlSchemas, enableRunCode,
        # enableTestMode, envInfo, libraryUrl, __typename,


    def generate_description(self, showHints=True, showSimiar=True, showURL=True, showTags=True):
        self.description = "\n===  Question === \n"
        self.description += bs(self.res['content'], 'lxml').get_text()
        self.description += "\n\n"

        # add hints
        if showHints:
            self.description += "\n===  Hints === \n"
            self.description += "\n".join([h for h in self.res['hints']])
            self.description += "\n\n"

        # add similar questions
        if showHints:
            self.description += "\n=== Similar Questions === \n"
            self.description += "\n".join([q["titleSlug"] for q in json.loads(self.res['similarQuestions'])])
            self.description += "\n\n"

        # add tags
        if showTags:
            self.description += "\n=== Tags === \n"
            self.description += ", ".join(list(map(lambda s: s.replace("-"," "), self.topic_tags)))
            self.description += "\n\n"

        # add link to leetcode website
        if showURL:
            self.description += "\n=== Question URL === \n"
            self.description += WEBSITE_URL + PROBLEM_EXTENTION + self.title_slug
            self.description += "\n\n"

        print(self.description)


    def generate_code_snippet(self, language="Python3"):
        for c in self.res['codeSnippets']:
            if c['lang'] == language:
                self.code_snippet = c['code']
        if self.code_snippet is None:
            raise NameError("Can't find your the languauge {}".format(language))


    def generate_sample_input(self):  # assuming there's only one input

        # get parameter value of sample test case
        arg_val = list(map(json.loads, self.res["sampleTestCase"].split("\n")))

        # get parameter name 
        arg_name = [i["name"] for i in json.loads(self.res["metaData"])["params"]]

        # combine name and value as a dict
        self.sample_input = {k:v for k, v in zip(arg_name, arg_val)}

