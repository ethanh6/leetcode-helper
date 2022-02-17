from LeetCodeHelper import *
import sys

if __name__ == '__main__':
    LCH = LeetcodeHelper(refresh_data=False)
    try:
        question_number = int(sys.argv[1])
        if question_number + 2 != len(sys.argv):
            exit("input not valid: {}".format(sys.argv))
        for i, q in enumerate(sys.argv):
            if int(i) < 2: continue
            LCH.build_question(q_id=int(i))

        LCH.build_working_dir_for_questions()
    except:
        exit("Somethine wrong with your input")


